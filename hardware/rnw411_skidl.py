#!/usr/bin/env python3
"""
RNW411 - Schema KiCad generato via SKiDL
=========================================
Replacement board per RDZ RNW411 basata su ESP32 + ESPHome

Uso:
  export KICAD_SYMBOL_DIR="/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols"
  python rnw411_skidl.py
  -> genera rnw411.net, rnw411.xml
"""

import os
from skidl import *

# ---------------------------------------------------------------------------
# Path librerie KiCad - modifica se necessario
# ---------------------------------------------------------------------------
KICAD_LIBS = os.environ.get(
    'KICAD_SYMBOL_DIR',
    '/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols'
)
lib_search_paths[KICAD].insert(0, KICAD_LIBS)

# ===========================================================================
# NETS
# ===========================================================================

vcc_5v         = Net('VCC_5V')
vcc_33v        = Net('VCC_3V3')
gnd            = Net('GND')
i2c_scl        = Net('I2C_SCL')
i2c_sda        = Net('I2C_SDA')

gpio_k1        = Net('GPIO_K1_COMPRESSORE')
gpio_k2        = Net('GPIO_K2_VALVOLA')
gpio_k3        = Net('GPIO_K3_VENT1')
gpio_k4        = Net('GPIO_K4_VENT2')
gpio_k5        = Net('GPIO_K5_VENT3')

gpio_id1       = Net('GPIO_ID1_PRESSOSTATO')
gpio_id2       = Net('GPIO_ID2_INTEGRAZIONE')
gpio_id3       = Net('GPIO_ID3_DEUMIDIFICAZIONE')
gpio_id4       = Net('GPIO_ID4_VENTILAZIONE')

ntc_s1         = Net('NTC_S1_EVAP')
ntc_s2         = Net('NTC_S2_ACQUA')

ac_fase        = Net('AC_FASE')
ac_fused_hlk   = Net('AC_FASE_HLK')
ac_fused_relay = Net('AC_FASE_RELAY')
ac_neutro      = Net('AC_NEUTRO')
ac_pe          = Net('AC_PE')

ac_out1        = Net('AC_OUT1_COMPRESSORE')
ac_out2        = Net('AC_OUT2_VALVOLA')
ac_out3        = Net('AC_OUT3_VENT1')
ac_out4        = Net('AC_OUT4_VENT2')
ac_out5        = Net('AC_OUT5_VENT3')

drv_k1         = Net('DRV_K1')
drv_k2         = Net('DRV_K2')
drv_k3         = Net('DRV_K3')
drv_k4         = Net('DRV_K4')
drv_k5         = Net('DRV_K5')

led_pwr        = Net('LED_PWR')
led_ok         = Net('LED_OK')
led_fault      = Net('LED_FAULT')

# ===========================================================================
# TEMPLATE PARTI  (nomi simbolo verificati su KiCad 6/7/8)
# ===========================================================================

# Device.kicad_sym
R_T    = Part('Device', 'R',              footprint='Resistor_SMD:R_0603_1608Metric',                             dest=TEMPLATE)
C_T    = Part('Device', 'C',              footprint='Capacitor_SMD:C_0603_1608Metric',                            dest=TEMPLATE)
CP_T   = Part('Device', 'C_Polarized',    footprint='Capacitor_THT:CP_Radial_D5.0mm_P2.00mm',                     dest=TEMPLATE)
CX2_T  = Part('Device', 'C',              footprint='Capacitor_THT:C_Disc_D5.1mm_W3.2mm_P2.50mm',                 dest=TEMPLATE)
D_T    = Part('Device', 'D',              footprint='Diode_SMD:D_SMA',                                            dest=TEMPLATE)
DTVS_T = Part('Device', 'D_TVS',          footprint='Diode_THT:D_DO-204AC_P12.70mm_Horizontal',                   dest=TEMPLATE)
DZ_T   = Part('Device', 'D_Zener',        footprint='Diode_SMD:D_SMA',                                            dest=TEMPLATE)
LED_T  = Part('Device', 'LED',            footprint='LED_THT:LED_D3.0mm',                                         dest=TEMPLATE)
FUSE_T = Part('Device', 'Fuse',           footprint='Fuse:Fuse_5x20mm_Schurter_0031_8201_Horizontal_Open',        dest=TEMPLATE)
VAR_T  = Part('Device', 'Varistor',       footprint='Varistor_THT:RV_Disc_D20mm_W3.8mm_P10mm',                    dest=TEMPLATE)
SW_T   = Part('Switch', 'SW_Push',        footprint='Button_Switch_THT:SW_PUSH_6mm',                              dest=TEMPLATE)

# Connector_Generic.kicad_sym  (NON 'Connector')
J1_T   = Part('Connector_Generic', 'Conn_01x01', footprint='Connector_PinHeader_5.08mm:PinHeader_1x01_P5.08mm_Vertical', dest=TEMPLATE)
J2_T   = Part('Connector_Generic', 'Conn_01x02', footprint='Connector_PinHeader_5.08mm:PinHeader_1x02_P5.08mm_Vertical', dest=TEMPLATE)
J3_T   = Part('Connector_Generic', 'Conn_01x03', footprint='Connector_PinHeader_5.08mm:PinHeader_1x03_P5.08mm_Vertical', dest=TEMPLATE)

# Relay_THT.kicad_sym
K10_T  = Part('Relay', 'G5LE-1-DC5',    footprint='Relay_THT:Relay_SPDT_Omron_G5LE',  dest=TEMPLATE)
K16_T  = Part('Relay', 'G5LE-14-DC5',   footprint='Relay_THT:Relay_SPDT_Omron_G5LE',  dest=TEMPLATE)

# Transistor_FET.kicad_sym
Q_T    = Part('Transistor_FET', 'AO3400A', footprint='Package_TO_SOT_SMD:SOT-23',       dest=TEMPLATE)

# ===========================================================================
# ALIMENTAZIONE - HLK-PM01 + AP2112K-3.3
# ===========================================================================

# Fusibili
F1 = FUSE_T(value='500mA/250V', ref='F1')
F2 = FUSE_T(value='10AT/250V',  ref='F2')
F1['~'] += ac_fase,        ac_fused_hlk   # pin 1,2
F2['~'] += ac_fase,        ac_fused_relay

# MOV
RV1 = VAR_T(value='S20K275', ref='RV1')
RV1[1] += ac_fase
RV1[2] += ac_neutro

# HLK-PM01 (Converter_ACDC)
U4 = Part('Converter_ACDC', 'HLK-PM01',
          footprint='Converter_ACDC:HLK-PM01', ref='U4')
U4['AC']  += ac_fused_hlk
U4['~AC'] += ac_neutro
U4['DC']  += vcc_5v
U4['~DC'] += gnd

# Bulk 5V
C10 = CP_T(value='100uF/10V', ref='C10')
C10['+'] += vcc_5v
C10['-'] += gnd

# AP2112K-3.3  (Regulator_Linear)
U3 = Part('Regulator_Linear', 'AP2112K-3.3',
          footprint='Package_TO_SOT_SMD:SOT-25', ref='U3')
U3['VI']  += vcc_5v
U3['VO']  += vcc_33v
U3['GND'] += gnd
U3['EN']  += vcc_5v

C11 = C_T(value='1uF/10V X5R', ref='C11')
C12 = C_T(value='1uF/10V X5R', ref='C12')
C11[1] += vcc_33v; C11[2] += gnd
C12[1] += vcc_5v;  C12[2] += gnd

# ===========================================================================
# ESP32-WROOM-32E  (RF_Module)
# ===========================================================================

U1 = Part('RF_Module', 'ESP32-WROOM-32',
          footprint='RF_Module:ESP32-WROOM-32', ref='U1')

U1['3V3']  += vcc_33v
U1['GND']  += gnd
U1['IO21'] += i2c_sda
U1['IO22'] += i2c_scl
U1['IO25'] += gpio_k1
U1['IO26'] += gpio_k2
U1['IO27'] += gpio_k3
U1['IO32'] += gpio_k4
U1['IO33'] += gpio_k5
U1['IO34'] += gpio_id1
U1['IO35'] += gpio_id2
U1['IO36'] += gpio_id3
U1['IO39'] += gpio_id4
U1['IO2']  += led_pwr
U1['IO4']  += led_ok
U1['IO5']  += led_fault

C14 = C_T(value='100nF', ref='C14')
C14[1] += vcc_33v; C14[2] += gnd

# ===========================================================================
# ADS1115  (Analog_ADC)
# ===========================================================================

U2 = Part('Analog_ADC', 'ADS1115IDGSR',
          footprint='Package_SO:SOIC-8_3.9x4.9mm_P1.27mm', ref='U2')

U2['VDD']  += vcc_33v
U2['GND']  += gnd
U2['SCL']  += i2c_scl
U2['SDA']  += i2c_sda
U2['ADDR'] += gnd
U2['AIN0'] += ntc_s1
U2['AIN1'] += ntc_s2

C13 = C_T(value='100nF', ref='C13')
C13[1] += vcc_33v; C13[2] += gnd

R10 = R_T(value='10k', ref='R10')
R11 = R_T(value='10k', ref='R11')
R10[1] += vcc_33v; R10[2] += ntc_s1
R11[1] += vcc_33v; R11[2] += ntc_s2

J8 = J2_T(value='NTC_S1', ref='J8')
J9 = J2_T(value='NTC_S2', ref='J9')
J8[1] += ntc_s1; J8[2] += gnd
J9[1] += ntc_s2; J9[2] += gnd

# ===========================================================================
# HELPER: canale relè
# ===========================================================================

def relay_channel(gpio_net, drv_net, ac_out_net,
                  ref_k, ref_q, ref_rg, ref_dfly,
                  ref_rsn, ref_csn, ref_dtvs,
                  is_16a=False):

    Rg = R_T(value='10k', ref=ref_rg)
    Rg[1] += gpio_net
    Rg[2] += drv_net

    Q = Q_T(value='AO3400A', ref=ref_q)
    Q['G'] += drv_net
    Q['S'] += gnd

    K = K16_T(ref=ref_k) if is_16a else K10_T(ref=ref_k)
    K['A1']  += vcc_5v
    K['A2']  += Q['D']
    K['COM'] += ac_fused_relay
    K['NO']  += ac_out_net

    Dfly = D_T(value='1N4007', ref=ref_dfly)
    Dfly['K'] += vcc_5v
    Dfly['A'] += K['A2']

    sn_mid = Net(ref_k + '_SN')
    Rsn = R_T(value='100R', ref=ref_rsn)
    Csn = CX2_T(value='100nF/275VAC X2', ref=ref_csn)
    Rsn[1] += ac_fused_relay; Rsn[2] += sn_mid
    Csn[1] += sn_mid;         Csn[2] += ac_out_net

    Dtvs = DTVS_T(value='P6KE250CA', ref=ref_dtvs)
    Dtvs['A'] += ac_out_net
    Dtvs['K'] += ac_fused_relay


relay_channel(gpio_k1, drv_k1, ac_out1, 'K1','Q1','R5', 'D1','R12','C1','D6',  is_16a=True)
relay_channel(gpio_k2, drv_k2, ac_out2, 'K2','Q2','R6', 'D2','R13','C2','D7')
relay_channel(gpio_k3, drv_k3, ac_out3, 'K3','Q3','R7', 'D3','R14','C3','D8')
relay_channel(gpio_k4, drv_k4, ac_out4, 'K4','Q4','R8', 'D4','R15','C4','D9')
relay_channel(gpio_k5, drv_k5, ac_out5, 'K5','Q5','R9', 'D5','R16','C5','D10')

# ===========================================================================
# HELPER: ingresso digitale
# ===========================================================================

def digital_input(gpio_net, ref_j, ref_r, ref_c, ref_d):
    J    = J2_T(ref=ref_j)
    Rin  = R_T(value='100R',  ref=ref_r)
    Cflt = C_T(value='100nF', ref=ref_c)
    Dtvs = DZ_T(value='SMAJ3V3A', ref=ref_d)

    filt = Net(ref_r + '_FILT')
    J[1]       += gnd
    J[2]       += Rin[1]
    Rin[2]     += filt
    Cflt[1]    += filt; Cflt[2] += gnd
    Dtvs['A']  += gnd
    Dtvs['K']  += filt
    filt        += gpio_net


digital_input(gpio_id1, 'J10', 'R1', 'C6',  'D11')
digital_input(gpio_id2, 'J11', 'R2', 'C7',  'D12')
digital_input(gpio_id3, 'J12', 'R3', 'C8',  'D13')
digital_input(gpio_id4, 'J13', 'R4', 'C9',  'D14')

# ===========================================================================
# CONNETTORI USCITE AC
# ===========================================================================

def ac_out_conn(ac_out_net, ref_j):
    J = J3_T(ref=ref_j)
    J[1] += ac_out_net
    J[2] += ac_neutro
    J[3] += ac_pe

ac_out_conn(ac_out1, 'J3')
ac_out_conn(ac_out2, 'J4')
ac_out_conn(ac_out3, 'J5')
ac_out_conn(ac_out4, 'J6')
ac_out_conn(ac_out5, 'J7')

J_AC = J2_T(ref='J1')
J_AC[1] += ac_fase; J_AC[2] += ac_neutro

J_PE = J1_T(ref='J2')
J_PE[1] += ac_pe

# ===========================================================================
# LED DI STATO
# ===========================================================================

def led_ch(gpio_net, ref_r, ref_d, color):
    Rl = R_T(value='1k', ref=ref_r)
    Dl = LED_T(value=f'LED_{color}_3mm', ref=ref_d)
    mid = Net(f'LED_{color}_MID')
    Rl[1] += vcc_33v; Rl[2] += mid
    Dl['K'] += gnd;   Dl['A'] += mid
    mid += gpio_net

led_ch(led_pwr,   'R17', 'LED1', 'ROSSO')
led_ch(led_ok,    'R18', 'LED2', 'VERDE')
led_ch(led_fault, 'R19', 'LED3', 'GIALLO')

# ===========================================================================
# PULSANTE BOOT / RESET
# ===========================================================================

SW1 = SW_T(ref='SW1')
SW1[1] += gnd
SW1[2] += U1['IO0']

# ===========================================================================
# GENERA NETLIST
# ===========================================================================

if __name__ == '__main__':
    ERC()
    generate_netlist(file_='rnw411.net')
    generate_xml(file_='rnw411.xml')
    print()
    print("=" * 60)
    print("  RNW411 - Netlist generata con successo!")
    print("=" * 60)
    print()
    print("  rnw411.net  -> KiCad PCBnew > File > Import Netlist")
    print("  rnw411.xml  -> ERC / BOM")
    print()
    print("  Clearance 230V: min 8mm")
    print("  Slot isolamento sotto relè")
    print("  GND plane DC separato da AC")
