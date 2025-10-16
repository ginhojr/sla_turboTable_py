import math

def min_max(value, min_val, max_val):
    """Helper function to constrain a value between min and max."""
    return min(max(value, min_val), max_val)

def erlang_b(servers, intensity):
    """Calculate the Erlang B formula."""
    try:
        if servers < 0 or intensity < 0:
            return 0
        val = intensity
        last = 1
        max_iterate = int(servers)  # Truncate to integer
        for count in range(1, max_iterate + 1):
            b = (val * last) / (count + (val * last))
            last = b
        return min_max(last, 0, 1)
    except Exception:
        return 0

def erlang_c(servers, intensity):
    """Calculate the probability of a call being queued (Erlang C)."""
    try:
        if servers < 0 or intensity < 0:
            return 0
        b = erlang_b(servers, intensity)
        c = b / (((intensity / servers) * b) + (1 - (intensity / servers)))
        return min_max(c, 0, 1)
    except Exception:
        return 0

def sla(agents, service_time, calls_per_hour, aht):
    """
    Calculate the service level achieved for the given number of agents.
    
    Args:
        agents (float): The number of agents available.
        service_time (float): Target answer time in seconds (e.g., 15).
        calls_per_hour (float): The number of calls received in one hour period.
        aht (float): The call duration including after call work in seconds (e.g., 180).
    
    Returns:
        float: Service level as a percentage (between 0 and 1).
    """
    try:
        birth_rate = calls_per_hour
        death_rate = 3600 / aht
        traffic_rate = birth_rate / death_rate
        utilisation = traffic_rate / agents
        if utilisation >= 1:
            utilisation = 0.99
        server = agents
        c = erlang_c(server, traffic_rate)
        sl_queued = 1 - c * math.exp((traffic_rate - server) * service_time / aht)
        return min_max(sl_queued, 0, 1)
    except Exception:
        return 0
    
print(sla(10, 15, 100, 180))