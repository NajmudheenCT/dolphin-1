import datetime
import time

from collections import namedtuple

VMAX_PERF_MIN_INTERVAL = 300

ARRAY_METRICS = ["HostIOs",
                 "HostMBWritten",
                 "ReadResponseTime",
                 "HostMBReads",
                 "HostReads",
                 "HostWrites",
                 "WriteResponseTime"
                 ]

DELFIN_ARRAY_METRICS = [
    "response_time",
    "throughput",
    "read_throughput",
    "write_throughput",
    "bandwidth",
    "read_bandwidth",
    "write_bandwidth"
]
def epoch_time_ms_now():
    ms = int(time.time() * 1000)
    return ms


def epoch_time_intervel_ago(interval_seconds=0):
    return int(epoch_time_ms_now() - (interval_seconds * 1000))


def generate_performance_payload(array, interval, metrics):
    return {'symmetrixId': str(array),
            "endDate": epoch_time_ms_now(),
            "startDate": epoch_time_intervel_ago(interval),
            "metrics": metrics,
            "dataFormat": "Average"}


def parse_performance_data(response):
    metrics_map = {}
    for metrics in response["resultList"]["result"]:
        # convert timestamp from unix epoch time to human readable
        # easier to see the output

        timestamp = metrics["timestamp"]
        for key, value in metrics.items():
            metrics_map[key]=metrics_map.get(key,{})
            metrics_map[key][timestamp] = value

    print(metrics_map)
    return metrics_map

def fill_array_performance_metrics(metric_list):
    # response_time
    read_response_values = metric_list['WriteResponseTime']
    write_response_values = metric_list['WriteResponseTime']
    response_time_values = {x: read_response_values.get(x, 0) + write_response_values.get(x, 0)
                            for x in set(read_response_values).union(write_response_values)}
    read_bandwidth_values = metric_list['HostMBReads']
    write_bandwidth_values = metric_list['HostMBWritten']
    bandwidth_values = {x: read_bandwidth_values.get(x, 0) + write_bandwidth_values.get(x, 0)
                        for x in set(read_bandwidth_values).union(write_bandwidth_values)}
    throughput_values = metric_list['HostIOs']
    read_throughput_values = metric_list['HostReads']
    write_throughput_values = metric_list['HostWrites']
    delfin_metrics = {'response_time': response_time_values, 'read_bandwidth': read_bandwidth_values,
                      'write_bandwidth': write_bandwidth_values, 'throughput': throughput_values,
                      'read_throughput': read_throughput_values, 'write_throughput': write_throughput_values,
                      'bandwidth': bandwidth_values}
    return delfin_metrics

MetricStruct = namedtuple("Metric", "name labels values")