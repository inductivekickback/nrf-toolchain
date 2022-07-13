# See Product Specifications for more information:
# - nRF5340: https://bit.ly/3IAPGcw
# - nrf52840: https://bit.ly/3z1saTd
RADIO_CURRENTS_3V_DCDC_0DBM_A = {
    'nrf52840': {
        'ISTART,TX,DCDC': 0.0052,
        'ITX,0dBM,DCDC': 0.0048,
        'ISTART,RX,1M,DCDC': 0.0037,
        'IRX,2M,DCDC': 0.0052
    },
    'nrf5340':  {
        'ISTART,TX,DCDC': 0.0024,
        'ITX,0dBM,DCDC': 0.0034,
        'ISTART,RX,1M,DCDC': 0.0021,
        'IRX,2M,DCDC': 0.0031
    }
}


def _on_air_len_2mbps_us(pl_len_bytes, pcf_bits, tx_mode):
    """ References:
    - Enhanced Shockburst packet description: https://bit.ly/3PafTky
    - tx_disable_us (tTXDISABLE,2M): https://bit.ly/3RhV9sT

    NOTE: Carrier is transmitted during TX_DISABLE.
    """
    preamble_bits = 8
    address_bits = 40
    crc_bits = 16
    pl_len_bits = (pl_len_bytes * 8)
    data_us = float(preamble_bits + address_bits + pcf_bits + pl_len_bits + crc_bits) / 2
    if tx_mode:
        tx_disable_us = 4
        return data_us + tx_disable_us
    return data_us


def _pkt_len_2mbps_us(pl_len_bytes, pcf_bits=11, ramp_up_us=40, tx_mode=False):
    """ References:
    - ramp_up_us (tTXEN,FAST)/(rRXEN,FAST): https://bit.ly/3RhV9sT
    """
    pkt_len_us = _on_air_len_2mbps_us(pl_len_bytes, pcf_bits, tx_mode)
    return ramp_up_us + pkt_len_us


def pkt_len_tx_2mbps_us(pl_len_bytes, pcf_bits=11, ramp_up_us=40):
    """"""
    return _pkt_len_2mbps_us(pl_len_bytes, pcf_bits, ramp_up_us, True)


def pkt_len_rx_2mbps_us(pl_len_bytes, pcf_bits=11, ramp_up_us=40):
    """ References:
    - rx_chain_us (tRXCHAIN,2M): https://bit.ly/3RhV9sT
    """
    rx_chain_us = 5
    return _pkt_len_2mbps_us(pl_len_bytes, pcf_bits, ramp_up_us) + rx_chain_us


def pkt_len_tx_w_ack_2mbps_us(pl_len_bytes, ack_pl_len_bytes, pcf_bits=11, ramp_up_us=40):
    tx_us = pkt_len_tx_2mbps_us(pl_len_bytes, pcf_bits, ramp_up_us)
    return tx_us + pkt_len_rx_2mbps_us(ack_pl_len_bytes, pcf_bits, ramp_up_us)


def pkt_len_rx_w_ack_2mbps_us(pl_len_bytes, ack_pl_len_bytes, pcf_bits=11, ramp_up_us=40):
    rx_us = pkt_len_rx_2mbps_us(pl_len_bytes, pcf_bits, ramp_up_us)
    return rx_us + pkt_len_tx_2mbps_us(ack_pl_len_bytes, pcf_bits, ramp_up_us)


def pkt_energy_tx_2mbps_j(pl_len_bytes, device_str, pcf_bits=11, ramp_up_us=40):
    """Standard measurements in the Product Specifications use VDD=3."""
    start_a = RADIO_CURRENTS_3V_DCDC_0DBM_A[device_str]['ISTART,TX,DCDC']
    tx_a = RADIO_CURRENTS_3V_DCDC_0DBM_A[device_str]['ITX,0dBM,DCDC']
    start_j = 3 * start_a * ramp_up_us / 1000000
    tx_j = 3 * tx_a * _on_air_len_2mbps_us(pl_len_bytes, pcf_bits, True) / 1000000
    return start_j + tx_j


def pkt_energy_rx_2mbps_j(pl_len_bytes, device_str, pcf_bits=11, ramp_up_us=40):
    """Standard measurements in the Product Specifications use VDD=3."""
    start_a = RADIO_CURRENTS_3V_DCDC_0DBM_A[device_str]['ISTART,RX,1M,DCDC']
    rx_a = RADIO_CURRENTS_3V_DCDC_0DBM_A[device_str]['IRX,2M,DCDC']
    start_j = 3 * start_a * ramp_up_us / 1000000
    rx_j = 3 * rx_a * _on_air_len_2mbps_us(pl_len_bytes, pcf_bits, False) / 1000000
    return start_j + rx_j


def pkt_energy_tx_w_ack_2mbps_j(pl_len_bytes, ack_pl_len_bytes, device_str, pcf_bits=11, ramp_up_us=40):
    """"""
    tx_j = pkt_energy_tx_2mbps_j(pl_len_bytes, device_str, pcf_bits, ramp_up_us)
    return tx_j + pkt_energy_rx_2mbps_j(ack_pl_len_bytes, device_str, pcf_bits, ramp_up_us)


def pkt_energy_rx_w_ack_2mbps_j(pl_len_bytes, ack_pl_len_bytes, device_str, pcf_bits=11, ramp_up_us=40):
    """"""
    rx_j = pkt_energy_rx_2mbps_j(pl_len_bytes, device_str, pcf_bits, ramp_up_us)
    return rx_j + pkt_energy_tx_2mbps_j(ack_pl_len_bytes, device_str, pcf_bits, ramp_up_us)
