/*
 * @file name: util-tools.h
 * on 2016/10/10.
 */

#ifndef _UTIL_TOOLS_H
#define _UTIL_TOOLS_H

#ifndef __USE_GNU
#define __USE_GNU
#endif
#include <sched.h>
#include <pthread.h>

#ifdef __cplusplus
extern "C" {
#endif

#define NOFILE                                1024

int daemon_init(void);
int thread_set_cpu(pthread_t pid, int cpu_index, int cpu_num);
inline uint16_t TCPCalculateChecksum(uint16_t *shdr, uint16_t *pkt,
                                            uint16_t tlen);
inline uint16_t IPV4CalculateChecksum(uint16_t *, uint16_t);

#ifdef __cplusplus
}
#endif

#endif //_UTIL_TOOLS_H
