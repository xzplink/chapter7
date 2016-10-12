/*
 * @file name: util-afpacket.c
 * Created by zhaozhang@yxlink.com
 * on 2016/10/10.
 */

#include <sys/errno.h>
#include <sys/ioctl.h>
#include <string.h>
#include "util-afpacket.h"
#include "util-tools.h"

#ifdef __cplusplus
extern "C" {
#endif

int get_nic_index(int fd, const char* nic_name)
{
    struct ifreq    ifr;

    if (nic_name == NULL)   return -1;

    memset(&ifr, 0, sizeof(ifr));
    strncpy(ifr.ifr_name, nic_name, IFNAMSIZ);

    if (ioctl(fd, SIOCGIFINDEX, &ifr) == -1) {
        printf("%s: SIOCGIFINDEX ioctl error: %s\n", __FUNCTION__, strerror(errno));
        return -1;
    }

    return ifr.ifr_ifindex;
}

static void destroy_instance(AFPacketInstance *instance)
{
    if (instance) {
        if (instance->fd != -1) {
            close(instance->fd);
        }
        if (instance->name) {
            free(instance->name);
            instance->name = NULL;
        }

        free(instance);
    }
}

static AFPacketInstance *create_instance(const char *device)
{
    AFPacketInstance *instance = NULL;
    struct ifreq ifr;

    //instance
    instance = calloc(1, sizeof(AFPacketInstance));
    if (!instance) {
        printf("%s: Could not allocate a new instance structure.\n", __FUNCTION__);
        goto err;
    }

    //instance->name
    if ((instance->name = strdup(device)) == NULL) {
        printf("%s: Could not allocate a copy of the device name.\n", __FUNCTION__);
        goto err;
    }

    //instance->fd
    instance->fd    = socket(PF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    if (instance->fd == -1) {
        printf("%s: Could not open the PF_PACKET socket: %s\n", __FUNCTION__, strerror(errno));
        goto err;
    }

    //instance->index
    instance->index = get_nic_index(instance->fd, instance->name);
    if (instance->index == -1) {
        printf("%s: Could not find index for device %s\n", __FUNCTION__, instance->name);
        goto err;
    }

    //instance->sll
    instance->sll.sll_family    = AF_PACKET;
    instance->sll.sll_ifindex   = instance->index;
    instance->sll.sll_protocol  = htons(ETH_P_ALL);

    //instance->sll.state
    instance->state             = STATE_STOPPED;

    return instance;
    err:
    destroy_instance(instance);
    return NULL;
}

static int bind_interface( AFPacketInstance *instance)
{
    int ret = 0;

    if (bind(instance->fd, (struct sockaddr *) &(instance->sll), sizeof(instance->sll)) != 0) {
        printf("%s: bind error: %s\n", __FUNCTION__, strerror(errno));
        ret = -1;
    }

    //check any pending errors
    int         err;
    socklen_t   errlen  = sizeof(err);
    if (getsockopt(instance->fd, SOL_SOCKET, SO_ERROR, &err, &errlen) || err)
    {
        printf("%s: getsockopt: %s", __FUNCTION__, strerror(errno));
        return AF_ERROR;
    }

    return ret;
}

static int set_nic_promisc(AFPacketInstance *instance)
{
    struct ifreq ethreq;
    int    ret = 0;

    strncpy(ethreq.ifr_name, instance->name, IFNAMSIZ);
    ioctl(instance->fd, SIOCGIFFLAGS, &ethreq);

    ethreq.ifr_flags |= IFF_PROMISC;
    ioctl(instance->fd, SIOCSIFFLAGS, &ethreq);

    return ret;
}

// Turn on promiscuous mode for the device.
static int set_nic_promisc_v2(AFPacketInstance *instance)
{
    struct packet_mreq  mr;

    memset(&mr, 0, sizeof(mr));
    mr.mr_ifindex   = instance->index;
    mr.mr_type      = PACKET_MR_PROMISC;
    if (setsockopt(instance->fd, SOL_PACKET, PACKET_ADD_MEMBERSHIP, &mr, sizeof(mr)) == -1)
    {
        printf("%s: setsockopt: %s", __FUNCTION__, strerror(errno));
        return AF_ERROR;
    }

    return AF_SUCCESS;
}

uint8_t afpacket_init(const char *dev_name, void **ctxt_ptr)
{
    AFPacketInstance    *instance;
    int ret  = 0;
//    printf("[*] enter into afpacket_init.\n");
    instance        = create_instance(dev_name);
    *ctxt_ptr       = instance;
    if(instance == NULL) {
//        printf("[*] instance is NULL.\n");
        ret = -1;
    }

    return ret;
}

static int iface_get_arptype(AFPacketInstance *instance)
{
    struct ifreq ifr;

    memset(&ifr, 0, sizeof(ifr));
    strncpy(ifr.ifr_name, instance->name, sizeof(ifr.ifr_name));
    if (ioctl(instance->fd, SIOCGIFHWADDR, &ifr) == -1)
    {
        return AF_ERROR;
    }

    return ifr.ifr_hwaddr.sa_family;
}

// The function below was heavily influenced by LibPCAP's pcap-linux.c.  Thanks!
static int determine_version(AFPacketInstance *instance)
{
    socklen_t   len;
    int         val;

    // Probe whether kernel supports TPACKET_V2
    val     = TPACKET_V2;
    len     = sizeof(val);
    if (getsockopt(instance->fd, SOL_PACKET, PACKET_HDRLEN, &val, &len) < 0)
    {
        return AF_ERROR;
    }
    instance->tp_hdrlen = val;

    /* Tell the kernel to use TPACKET_V2 */
    val = TPACKET_V2;
    if (setsockopt(instance->fd, SOL_PACKET, PACKET_VERSION, &val, sizeof(val)) < 0)
    {
        return AF_ERROR;
    }
    instance->tp_version = TPACKET_V2;

    /* Reserve space for VLAN tag reconstruction */
    val = VLAN_TAG_LEN;
    if (setsockopt(instance->fd, SOL_PACKET, PACKET_RESERVE, &val, sizeof(val)) < 0)
    {
        return AF_ERROR;
    }

    return AF_SUCCESS;
}

static void reset_stats(AFPacketInstance *instance)
{
    memset(&instance->state, 0, sizeof(uint8_t));

    struct      tpacket_stats kstats;
    socklen_t   len = sizeof (struct tpacket_stats);
    getsockopt(instance->fd, SOL_PACKET, PACKET_STATISTICS, &kstats, &len);
}

int afpacket_start(void *handle)
{
    int ret = 0;
    AFPacketInstance *instance = (AFPacketInstance *) handle;

    ret = bind_interface(instance);
    ret = set_nic_promisc(instance);
    instance->state = STATE_STARTED;

    return ret;
}

int afpacket_start_v2(void *handle)
{
    AFPacketInstance *instance = (AFPacketInstance *) handle;

    //bind
    if (bind_interface(instance) != AF_SUCCESS)
    {
        printf("bind fail!\n");
        return AF_ERROR;
    }

    //set promiscuous
    if (set_nic_promisc(instance) != AF_SUCCESS)
    {
        return AF_ERROR;
    }

    //get the link-layer type
    int     arptype;
    arptype     = iface_get_arptype(instance);
    if (arptype < 0)
    {
        printf("get arptype fail!\n");
        return AF_ERROR;
    }
    if (arptype != ARPHRD_ETHER)
    {
        printf("arptype != ARPHRD_ETHER!\n");
        return AF_ERROR;
    }

    //determine TPACKET_V2
    if (determine_version(instance) != AF_SUCCESS)
    {
        printf("determine_version fail!\n");
        return AF_ERROR;
    }
    //reset_stats
//    reset_stats(instance);
}

int afpacket_acquire(void *handle, Packet *p, uint32_t pkt_len)
{
    AFPacketInstance *instance  = (AFPacketInstance *) handle;
    int  fromlen                = 0;
    uint8_t  *pkt               = p->pkt;


    fromlen = recv(instance->fd, pkt, 2000, MSG_TRUNC);
    if (fromlen>0) {
        //mac
        p->ethh = (EtherHdr *) pkt;
        if (p->ethh && (ntohs(p->ethh->ether_type) != IP_TYPE)) {
            return 0;
        }

        //IP
        p->ip4h = (IP4Hdr *)(pkt+sizeof(EtherHdr));
        if (p->ip4h && (p->ip4h->ip_proto != TCP_TYPE)) {
            return 0;
        }

        //TCP
        p->tcph = (TCPHdr *)(p->ip4h + IPV4_GET_HLEN(p));
        if (p->tcph && (ntohs(p->tcph->th_dport) != HTTP_PORT)) {
            return 0;
        }
    }

    return fromlen;
}

int afpacket_send(void *handle, Packet *p)
{
    AFPacketInstance *instance  = (AFPacketInstance *) handle;
    int  send_success           = 0;

    send_success    = send(instance->fd, p->pkt, p->pkt_len, MSG_DONTROUTE);

    return send_success;
}

int afpacket_close(void *handle)
{
    int ret = 0;
    AFPacketInstance *instance = (AFPacketInstance *) handle;

    destroy_instance(instance);
    instance->state = STATE_STOPPED;

    return ret;
}

Packet *exchange_for_respond_pkt(Packet *p, uint8_t flag)
{
    printf("111111111111111111\n");
    /* Swap layer 2 info. */
    uint8_t ether_tmp[6];
    memcpy(ether_tmp, p->ethh->ether_dst, 6*sizeof(uint8_t));
    memcpy(p->ethh->ether_dst, p->ethh->ether_src, 6*sizeof(uint8_t));
    memcpy(p->ethh->ether_src, ether_tmp, 6*sizeof(uint8_t));
    printf("2222222222222222222\n");
    /* Swap layer 3 info. */
    struct in_addr ip_tmp;
    memcpy(&ip_tmp, &p->ip4h->s_ip_src, sizeof(struct in_addr));
    memcpy(&p->ip4h->s_ip_src, &p->ip4h->s_ip_dst, sizeof(struct in_addr));
    memcpy(&p->ip4h->s_ip_dst, &ip_tmp, sizeof(struct in_addr));
    printf("333333333333333333\n");
    /* Swap layer 4 info. */
    uint16_t port_tmp;
    port_tmp = p->tcph->th_sport;
    p->tcph->th_sport = p->tcph->th_dport;
    p->tcph->th_dport = port_tmp;
    if(flag){
        p->tcph->th_flags |= flag;
    }
    printf("444444444444444444\n");

    return p;
}

int ReCalculateChecksum(Packet *p)
{
    if (PKT_IS_IPV4(p)) {
        if (PKT_IS_TCP(p)) {
            /* TCP */
            p->tcph->th_sum = 0;
            p->tcph->th_sum = TCPCalculateChecksum(p->ip4h->s_ip_addrs,
                                                   (uint16_t *)p->tcph, (p->payload_len + TCP_GET_HLEN(p)));
        }
        /* IPV4 */
        p->ip4h->ip_csum = 0;
        p->ip4h->ip_csum = IPV4CalculateChecksum((uint16_t *)p->ip4h,
                                                 IPV4_GET_RAW_HLEN(p->ip4h));
    }

    return 0;
}

int print_packet_info(Packet *p)
{
    EtherHdr    *ethh = NULL;
    IP4Hdr      *ip4h = NULL;
    TCPHdr      *tcph = NULL;
    uint8_t     *pkt  = p->pkt;

    if(p == NULL || pkt == NULL){
        return -1;
    }
    ethh = (EtherHdr *)pkt;
    printf("|+|---------------------------|+|\n");
    printf("|-| mac type: %d\n", ethh->ether_type);
    char mac_dst[32]= {0}, mac_src[32] = {0};
    sprintf(mac_dst,"%02x:%02x:%02x:%02x:%02x:%02x",
            ethh->ether_dst[0],
            ethh->ether_dst[1],
            ethh->ether_dst[2],
            ethh->ether_dst[3],
            ethh->ether_dst[4],
            ethh->ether_dst[5]
            );
    sprintf(mac_src,"%02x:%02x:%02x:%02x:%02x:%02x",
            ethh->ether_src[0],
            ethh->ether_src[1],
            ethh->ether_src[2],
            ethh->ether_src[3],
            ethh->ether_src[4],
            ethh->ether_src[5]
    );
    printf("|-| mac_dst: %s\n", mac_dst);
    printf("|-| mac_src: %s\n", mac_src);

    ip4h = (IP4Hdr *)(pkt + sizeof(EtherHdr));
    printf("|-| proto: %d\n", ip4h->ip_proto);
    printf("|-| ip_src: %s\n", inet_ntoa(ip4h->s_ip_src));
    printf("|-| ip_dst: %s\n", inet_ntoa(ip4h->s_ip_dst));
//    printf("|-| ip_csum: %s\n", ntohs(ip4h->ip_csum));

    tcph = (TCPHdr *)(ip4h + IPV4_GET_HLEN(p));
    printf("|-| sport: %d\n", ntohs(tcph->th_sport));
    printf("|-| dport: %d\n", ntohs(tcph->th_dport));
    printf("|-| th_offx2: %d\n", tcph->th_offx2);
//    printf("|-| th_sum: %d\n", ntohs(tcph->th_sum));
    printf("|+|---------------------------|+|\n");

    return 0;
}

#ifdef __cplusplus
}
#endif
