/*
 * @file name: util-tools.h
 * Created by zhaozhang@yxlink.com
 * on 2016/10/10.
 */

#ifndef _UTIL_TOOLS_H
#define _UTIL_TOOLS_H

#include <pthread.h>

#define PKT_IS_IPV4(p)      (((p)->ip4h != NULL))
#define PKT_IS_TCP(p)       (((p)->tcph != NULL))
#define PKT_IS_UDP(p)       (((p)->udph != NULL))

#define TH_FIN                               0x01
#define TH_SYN                               0x02
#define TH_RST                               0x04
#define TH_PUSH                              0x08
#define TH_ACK                               0x10
#define TH_URG                               0x20
/** Establish a new connection reducing window */
#define TH_ECN                               0x40
/** Echo Congestion flag */
#define TH_CWR                               0x80

#define TCP_GET_RAW_OFFSET(tcph)             (((tcph)->th_offx2 & 0xf0) >> 4)
#define TCP_GET_OFFSET(p)                    TCP_GET_RAW_OFFSET((p)->tcph)
#define TCP_GET_HLEN(p)                      (TCP_GET_OFFSET((p)) << 2)

int daemon_init(void);
int thread_set_cpu(pthread_t pid, int cpu_index, int cpu_num);
static inline uint16_t TCPCalculateChecksum(uint16_t *shdr, uint16_t *pkt,
                                            uint16_t tlen);
static inline uint16_t IPV4CalculateChecksum(uint16_t *, uint16_t);

#endif //_UTIL_TOOLS_H
