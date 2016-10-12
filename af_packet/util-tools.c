/*
 * @file name: util-tools.c
 * Created by zhaozhang@yxlink.com
 * on 2016/10/10.
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include <sys/stat.h>
#include <fcntl.h>
#include "ether-type.h"
#include "util-tools.h"

int daemon_init(void)
{
    pid_t pid;
    int i;

    if ((pid = fork()) < 0)  // fork error
        return(-1);
    else if(pid != 0)
        exit(0); /* parent exit */


    /* child continues */
    setsid(); /* become session leader */


    if ((pid=fork()) < 0) //fork error
        return(-1);
    else if (pid!=0)
        exit(0);  // the first child exit

    /* the child of the first child */

    for (i=0; i < NOFILE; i++) // because a lot of codes still use stdout, stderr,  keep them open....
        close(i);

    int fd;
    // redirect the stdin, stdout, stderr to /dev/null
    fd = open ("/dev/null", O_RDWR, 0);
    if (fd != -1)
    {
        dup2 (fd, STDIN_FILENO);
        dup2 (fd, STDOUT_FILENO);
        dup2 (fd, STDERR_FILENO);

        if (fd > 2)
            close (fd);
    }

    chdir("/"); /* change working directory */
    umask(0); /* clear file mode creation mask */

    return(0);
}

int thread_set_cpu(pthread_t pid, int cpu_index, int cpu_num)
{
    cpu_set_t   mask;
    cpu_set_t   get;
    int         i;


    CPU_ZERO(&mask);
    CPU_SET(cpu_index, &mask);
    if (pthread_setaffinity_np(pid, sizeof(mask), &mask) < 0)
    {
        printf("set thread affinity process%d failed!\n", cpu_index);
        return 0;
    }
    CPU_ZERO(&get);
    if (pthread_getaffinity_np(pid, sizeof(get), &get) < 0)
    {
        printf("get thread affinity process%d failed!\n", cpu_index);
        return 0;
    }
    for (i=0; i<cpu_num; i++)
    {
        if (CPU_ISSET(i, &get))
        {
            printf("thread %u is running in processor %d\n", (uint32_t)pid, i);
        }
    }

    return 1;
}

/**
 * \brief Calculates the checksum for the TCP packet
 *
 * \param shdr Pointer to source address field from the IP packet.  Used as a
 *             part of the pseudoheader for computing the checksum
 * \param pkt  Pointer to the start of the TCP packet
 * \param tlen Total length of the TCP packet(header + payload)
 *
 * \retval csum Checksum for the TCP packet
 */
inline uint16_t TCPCalculateChecksum(uint16_t *shdr, uint16_t *pkt,
                                            uint16_t tlen)
{
    uint16_t pad = 0;
    uint32_t csum = shdr[0];

    csum += shdr[1] + shdr[2] + shdr[3] + htons(6) + htons(tlen);

    csum += pkt[0] + pkt[1] + pkt[2] + pkt[3] + pkt[4] + pkt[5] + pkt[6] +
            pkt[7] + pkt[9];

    tlen -= 20;
    pkt += 10;

    while (tlen >= 32) {
        csum += pkt[0] + pkt[1] + pkt[2] + pkt[3] + pkt[4] + pkt[5] + pkt[6] +
                pkt[7] + pkt[8] + pkt[9] + pkt[10] + pkt[11] + pkt[12] + pkt[13] +
                pkt[14] + pkt[15];
        tlen -= 32;
        pkt += 16;
    }

    while(tlen >= 8) {
        csum += pkt[0] + pkt[1] + pkt[2] + pkt[3];
        tlen -= 8;
        pkt += 4;
    }

    while(tlen >= 4) {
        csum += pkt[0] + pkt[1];
        tlen -= 4;
        pkt += 2;
    }

    while (tlen > 1) {
        csum += pkt[0];
        pkt += 1;
        tlen -= 2;
    }

    if (tlen == 1) {
        *(uint8_t *)(&pad) = (*(uint8_t *)pkt);
        csum += pad;
    }

    csum = (csum >> 16) + (csum & 0x0000FFFF);
    csum += (csum >> 16);

    return (uint16_t)~csum;
}

/**
 * \brief Calculates the checksum for the IP packet
 *
 * \param pkt  Pointer to the start of the IP packet
 * \param hlen Length of the IP header
 *
 * \retval csum Checksum for the IP packet
 */
inline uint16_t IPV4CalculateChecksum(uint16_t *pkt, uint16_t hlen)
{
    uint32_t csum = pkt[0];

    csum += pkt[1] + pkt[2] + pkt[3] + pkt[4] + pkt[6] + pkt[7] + pkt[8] +
            pkt[9];

    hlen -= 20;
    pkt += 10;

    if (hlen == 0) {
        ;
    } else if (hlen == 4) {
        csum += pkt[0] + pkt[1];
    } else if (hlen == 8) {
        csum += pkt[0] + pkt[1] + pkt[2] + pkt[3];
    } else if (hlen == 12) {
        csum += pkt[0] + pkt[1] + pkt[2] + pkt[3] + pkt[4] + pkt[5];
    } else if (hlen == 16) {
        csum += pkt[0] + pkt[1] + pkt[2] + pkt[3] + pkt[4] + pkt[5] + pkt[6] +
                pkt[7];
    } else if (hlen == 20) {
        csum += pkt[0] + pkt[1] + pkt[2] + pkt[3] + pkt[4] + pkt[5] + pkt[6] +
                pkt[7] + pkt[8] + pkt[9];
    } else if (hlen == 24) {
        csum += pkt[0] + pkt[1] + pkt[2] + pkt[3] + pkt[4] + pkt[5] + pkt[6] +
                pkt[7] + pkt[8] + pkt[9] + pkt[10] + pkt[11];
    } else if (hlen == 28) {
        csum += pkt[0] + pkt[1] + pkt[2] + pkt[3] + pkt[4] + pkt[5] + pkt[6] +
                pkt[7] + pkt[8] + pkt[9] + pkt[10] + pkt[11] + pkt[12] + pkt[13];
    } else if (hlen == 32) {
        csum += pkt[0] + pkt[1] + pkt[2] + pkt[3] + pkt[4] + pkt[5] + pkt[6] +
                pkt[7] + pkt[8] + pkt[9] + pkt[10] + pkt[11] + pkt[12] + pkt[13] +
                pkt[14] + pkt[15];
    } else if (hlen == 36) {
        csum += pkt[0] + pkt[1] + pkt[2] + pkt[3] + pkt[4] + pkt[5] + pkt[6] +
                pkt[7] + pkt[8] + pkt[9] + pkt[10] + pkt[11] + pkt[12] + pkt[13] +
                pkt[14] + pkt[15] + pkt[16] + pkt[17];
    } else if (hlen == 40) {
        csum += pkt[0] + pkt[1] + pkt[2] + pkt[3] + pkt[4] + pkt[5] + pkt[6] +
                pkt[7] + pkt[8] + pkt[9] + pkt[10] + pkt[11] + pkt[12] + pkt[13] +
                pkt[14] + pkt[15] + pkt[16] + pkt[17] + pkt[18] + pkt[19];
    }

    csum = (csum >> 16) + (csum & 0x0000FFFF);
    csum += (csum >> 16);

    return (uint16_t) ~csum;
}

