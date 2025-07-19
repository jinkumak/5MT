import streamlit as st
import serial

# Set up serial connection
ser = serial.Serial('/dev/tty.usbmodem143201', 115200, timeout=1)

def convert_2bytes(val):
    return val.to_bytes(2, 'big')

def send_command(finger_ids, pos, speed, current, direction):
    header = bytes([0xAA, 0x55])
    finger_bytes = [0] * 5
    for fid in finger_ids:
        if 1 <= fid <= 5:
            finger_bytes[fid - 1] = 1
    finger_bytes = bytes(finger_bytes)

    pos_bytes = convert_2bytes(pos)
    speed_bytes = convert_2bytes(speed)
    current_bytes = convert_2bytes(current)
    direction = bytes([direction])

    data = finger_bytes  + speed_bytes + current_bytes + pos_bytes + direction
    checksum = 0
    for b in data:
        checksum ^= b
    full_command = header + data + bytes([checksum])
    
    ser.write(full_command)

# Streamlit UI
st.title("Robotic Hand Controller")

st.subheader("Select Fingers to Move")
finger_ids = []
for i in range(1, 6):
    if st.checkbox(f"Finger {i}", value=False):
        finger_ids.append(i)

position = st.slider("Position", 0, 400, 200)
speed = st.slider("Speed", 300, 3000, 1000)
current = st.slider("Current", 600, 1200, 1000)
direction = st.radio("Direction", [0, 1, 2], index=0)

if st.button("Send Command"):
    if finger_ids:
        send_command(finger_ids, position, speed, current, direction)
        st.success("Command sent!")
    else:
        st.warning("Please select at least one finger.")
