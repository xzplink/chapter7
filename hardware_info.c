// @filename hardware_info.cpp
// Created by zhaozhang@yxlink.com
// on 2017/6/2.
//
#define _BSD_SOURCE	/* for strtoll() */
//#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
//#define __USE_GNU	/* for O_DIRECT */
#include <string.h>
#include <fcntl.h>
#include <errno.h>
#include <linux/types.h>
#include <sys/ioctl.h>

#define	HDIO_GET_IDENTITY	 0x030d

static char *strip (char *s)
{
    char *e;

    while (*s == ' ') ++s;
    if (*s)
        for (e = s + strlen(s); *--e == ' '; *e = '\0');
    return s;
}

char *get_hard_disk_serno(char *devname)
{
    int fd;
    int err = 0;

    // char name[] = "/dev/sda";
    if (devname == NULL)
        return NULL;

    static int open_flags = O_RDONLY|O_NONBLOCK;

    fd = open(devname, open_flags);
    if (fd < 0)
    {
        err = errno;
        perror(devname);
    }
    else
    {
        __u16 id[256];

        if (!ioctl(fd, HDIO_GET_IDENTITY, id))
        {
            char *serno = strip(strndup((char *)&id[10], 20));

            //printf("HD serial: %s", serno);

            return serno;
        }
        else if (errno == -ENOMSG)
        {
            //printf("No identification info available\n");
        }
        else
        {
            err = errno;
            //perror("HDIO_GET_IDENTITY failed");
        }
    }
    return NULL;
}

#define cpuid(in,a,b,c,d) asm("cpuid": "=a" (a), "=b" (b), "=c" (c), "=d" (d) : "a" (in));
int get_cpu_id(char *cpu_id)
{
    unsigned long eax, ebx, ecx, edx;

    if(cpu_id == NULL){
        return -1;
    }
    cpuid (1, eax, ebx, ecx, edx);
    snprintf (cpu_id, 33, "%08lx%08lx%08lx%08lx", eax, ebx, ecx, edx);

    return 0;
}

int get_cpu_core_number()
{
    char buf[256];
    char cmd[] = "cat /proc/cpuinfo|grep pro|wc -l";
    FILE *fp = NULL;
    int ret = 0;

    if((fp = popen(cmd, "r")) != NULL) {
        if(fgets(buf, sizeof(buf), fp) != NULL){
            ret = atoi(buf);
        }
        pclose(fp);
    }

    return  ret;
}

int get_cpu_type(char *type)
{
    char buf[256];
    char cmd[] = "cat /proc/cpuinfo|grep name|cut -f2 -d:|head -1";
    FILE *fp = NULL;

    if(type == NULL){
        return -1;
    }

    if((fp = popen(cmd, "r")) != NULL) {
        if(fgets(buf, sizeof(buf), fp) != NULL){
            snprintf(type, sizeof(buf), "%s", buf);
        }
        pclose(fp);
    }

    return  0;
}

int get_motherboard_uuid(char *uuid)
{
    char buf[256];
    char cmd[] = "/usr/sbin/dmidecode -s system-uuid";
    FILE *fp = NULL;

    if(uuid == NULL){
        return -1;
    }

    if((fp = popen(cmd, "r")) != NULL) {
        if(fgets(buf, sizeof(buf), fp) != NULL){
            snprintf(uuid, sizeof(buf), "%s", buf);
        }
        pclose(fp);
    }

    return  0;
}

int get_mac_list(char *list)
{
    char buf[256];
    char cmd[] = "grep 'ATTR{address}' /etc/udev/rules.d/70-persistent-net.rules|awk -F ',' '{print $4}'|cut -d'\"' -f2";
    FILE *fp = NULL;
    char *tmp = list;

    if (list == NULL){
        return -1;
    }
    int idx = 0;
    if((fp = popen(cmd, "r")) != NULL) {
        while(fgets(buf, sizeof(buf), fp) != NULL){
            printf("mac is: %s", buf);
            int len = strlen(buf); // replace '\n' to ','
            buf[len-1] = ',';
            sprintf(tmp, "%s", buf);
            tmp = tmp + strlen(buf);
        }

        pclose(fp);
    }

    return  0;
}

int get_memory_total()
{
    char buf[256];
    char cmd[] = "free -m|grep Mem|awk '{print int($2/1000+0.99)}'";
    FILE *fp = NULL;
    int ret = 0;

    if((fp = popen(cmd, "r")) != NULL) {
        if(fgets(buf, sizeof(buf), fp) != NULL){
            ret = atoi(buf);
        }
        pclose(fp);
    }

    return  ret;
}

int get_system_time_now(char *time)
{
    char buf[256];
    char cmd[] = "/bin/date +%Y%m%d";
    FILE *fp = NULL;

    if(time == NULL){
        return -1;
    }

    if((fp = popen(cmd, "r")) != NULL) {
        if(fgets(buf, sizeof(buf), fp) != NULL){
            snprintf(time, sizeof(buf), "%s", buf);
        }
        pclose(fp);
    }

    return  0;
}

int main()
{
    char *serno = NULL;
    char hd_name[] = "/dev/sda";
    char cpuid[128];
    char motherboard_uuid[128];
    char mac_list[256];
    char cpu_type[256];
    char time[128];

    serno = get_hard_disk_serno(hd_name);
    printf("hard disk %s serno is: %s\n", hd_name, serno);

    get_cpu_id(cpuid);
    printf("cpu id is: %s\n", cpuid);

    get_motherboard_uuid(motherboard_uuid);
    printf("motherboard uuid is :%s\n", motherboard_uuid);

    get_mac_list(mac_list);
    printf("ehter mac list is :%s\n", mac_list);

    get_cpu_type(cpu_type);
    printf("cpu type is :%s\n", cpu_type);

    int num = get_cpu_core_number();
    printf("cpu num is : %d\n", num);

    int total = get_memory_total();
    printf("memory total is :%d\n", total);

    get_system_time_now(time);
    printf("system time now is: %s\n", time);

}

