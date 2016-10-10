/*
 * @file name: util-tools.h
 * Created by zhaozhang@yxlink.com
 * on 2016/10/10.
 */

#ifndef _UTIL_TOOLS_H
#define _UTIL_TOOLS_H

#include <pthread.h>

int daemon_init(void);
int thread_set_cpu(pthread_t pid, int cpu_index, int cpu_num);

#endif //_UTIL_TOOLS_H
