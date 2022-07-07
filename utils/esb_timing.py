def _pkt_len_2mbps_us(pl_len_bytes, pcf_bits=11, ramp_up_us=40):
    """ References:
    - Enhanced Shockburst packet description can be found here: https://bit.ly/3PafTky
    - ramp_up_us (tTXEN,FAST)/(rRXEN,FAST): https://bit.ly/3RhV9sT
    """
    preamble_bits = 8
    address_bits = 40
    crc_bits = 16
    pl_len_bits = (pl_len_bytes * 8)
    pkt_len_us = float(preamble_bits + address_bits + pcf_bits + pl_len_bits + crc_bits) / 2
    return (ramp_up_us + pkt_len_us)


def pkt_len_tx_2mbps_us(pl_len_bytes, pcf_bits=11, ramp_up_us=40):
    """ References:
    - tx_disable_us (tTXDISABLE,2M): https://bit.ly/3RhV9sT
    """
    tx_disable_us = 4
    return (_pkt_len_2mbps_us(pl_len_bytes, pcf_bits, ramp_up_us) + tx_disable_us)


def pkt_len_rx_2mbps_us(pl_len_bytes, pcf_bits=11, ramp_up_us=40):
    """ References:
    - rx_chain_us (tRXCHAIN,2M): https://bit.ly/3RhV9sT
    """
    rx_chain_us = 5
    return (_pkt_len_2mbps_us(pl_len_bytes, pcf_bits, ramp_up_us) + rx_chain_us)


def pkt_w_ack_len_2mbps_us(tx_pl_len_bytes, ack_pl_len_bytes, pcf_bits=11, ramp_up_us=40):
    tx_us = pkt_len_tx_2mbps_us(tx_pl_len_bytes, pcf_bits, ramp_up_us)
    return tx_us + pkt_len_rx_2mbps_us(ack_pl_len_bytes, pcf_bits, ramp_up_us)
  
