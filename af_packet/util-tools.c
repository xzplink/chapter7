/*
 * @file name: util-tools.c
 * Created by zhaozhang@yxlink.com
 * on 2016/10/10.
 */


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

    for (i=0; i<NOFILE;i++) // because a lot of codes still use stdout, stderr,  keep them open....
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
            printf("thread %d is running in processor %d\n", (int)pid, i);
        }
    }

    return 1;
}
