def check_nmea_checksum(nmea_sentence):
    split_sentence = nmea_sentence.split('*')
    if len(split_sentence) != 2:
        return False
    transmitted_checksum = split_sentence[1].strip()

    data_to_checksum = split_sentence[0][1:]
    checksum = 0
    for c in data_to_checksum:
        checksum ^= ord(c)

    return ("%02X" % checksum) == transmitted_checksum.upper()
