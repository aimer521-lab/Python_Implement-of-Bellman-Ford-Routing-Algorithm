import argparse
import json
from socket import *
import time


INNERNAME1 = 'distance'
INNERNAME2 = 'next_hop'


def _argparse():
    parser = argparse.ArgumentParser(description='input current node')
    parser.add_argument('--node', action='store', required=True, dest='node', help='this node')
    return parser.parse_args().node


# sender, sending node and distance dictionary
def vertex_sender(addr, my_node, vector):
    for ip in addr:
        udp_client = socket(AF_INET, SOCK_DGRAM)
        send_vector = json.dumps(vector)
        data = my_node.encode() + '?'.encode() + send_vector.encode()
        udp_client.sendto(data, tuple(addr.get(ip)))
        print(ip + 'sent')
        udp_client.close()


# main working flow
def main():
    # read initial information
    my_node = _argparse()
    with open(my_node + '_ip.json', 'r')as fp:  # ip information
        ip_info = json.load(fp)
    with open(my_node + '_distance.json', 'r')as fp2:   # initial distance table
        distance_info = json.load(fp2)

    # bind UDP server port, and initial distance
    udp_server = socket(AF_INET, SOCK_DGRAM)
    for ip in ip_info:
        current_addr = ip_info.get(ip)
        if ip == my_node:
            port = current_addr[1]
            udp_server.bind(('', port))
            print('port bound')

    # send once when start
    ip_info.pop(my_node)
    vertex_sender(ip_info, my_node, distance_info)

    # initialize output
    output_dict = {}
    for node, distance in distance_info.items():
        inner_dict = {INNERNAME1: distance, INNERNAME2: node}
        output_dict[node] = inner_dict
    with open(my_node + '_output.json', 'w')as ofp:
        json.dump(output_dict, ofp)

    # main algorithm part
    while True:
        # receiver
        print('waiting')
        data, addr = udp_server.recvfrom(20480)
        recv_node, recv_vector = data.decode().split('?')
        recv_vector = json.loads(recv_vector)
        print('received from ' + recv_node)

        # decider
        recv_vector.pop(my_node)
        for node, node_distance in recv_vector.items():
            if node not in distance_info:   # new path
                print('new path find')
                distance_info[node] = node_distance + distance_info[recv_node]
                inner_dict = {INNERNAME1: node_distance + distance_info[recv_node], INNERNAME2: recv_node}
                output_dict[node] = inner_dict
            elif distance_info[recv_node] + node_distance < distance_info[node]:    # shorter path
                print('shorter path find')
                distance_info[node] = distance_info[recv_node] + node_distance
                inner_dict = {INNERNAME1: distance_info[recv_node] + node_distance, INNERNAME2: recv_node}
                output_dict[node] = inner_dict

        # output result
        with open(my_node + '_output.json', 'w')as ofp:
            json.dump(output_dict, ofp)

        time.sleep(3)
        vertex_sender(ip_info, my_node, distance_info)


if __name__ == '__main__':
    main()