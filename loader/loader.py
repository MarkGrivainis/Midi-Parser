import typing

def parse_meta_event(file_handler):
    """TODO: Docstring for parse_meta_event.

    :file_handler: TODO
    :returns: TODO

    """
    meta_type = int.from_bytes(file_handler.read(1), byteorder='big')
    assert meta_type <= 128, 'Meta-Event type > 128'
    print('Meta-type:\t', meta_type)
    event_length = 0
    while True:
        byte = int.from_bytes(file_handler.read(1), byteorder='big')
        event_length += byte 
        if byte <= 128:
            break
    print('Event Length:\t', event_length)
    print('Content:\t', file_handler.read(event_length))


def parse_track(file_handler: typing.BinaryIO):
    """TODO: Docstring for parse_track.

    :file_handler: typing.B: TODO
    :returns: TODO

    """
    assert 'MTrk' == file_handler.read(4).decode('ascii'), 'header magic string is incorrect'
    track_length = int.from_bytes(file_handler.read(4), byteorder='big')
    for i in range(1):
        print('-----')
        delta_time = 0
        while True:
            byte = int.from_bytes(file_handler.read(1), byteorder='big')
            delta_time += byte 
            if byte <= 128:
                break

        event_type = file_handler.read(1)
        print('Delta Time:\t', delta_time)
        print('Event Type:\t', event_type)
        if event_type == b'\xFF':
            parse_meta_event(file_handler)
    for b in file_handler.read():
        print(b)


def parse_header(file_handler: typing.BinaryIO):
    """Function which handles converting bytes to values.
    :returns: TODO

    """
    assert 'MThd' == file_handler.read(4).decode('ascii'), 'header magic string is incorrect'
    assert 6 == int.from_bytes(file_handler.read(4), byteorder='big'), 'header "length" is incorrect'
    format = int.from_bytes(file_handler.read(2), byteorder='big')
    number_of_tracks = int.from_bytes(file_handler.read(2), byteorder='big')
    if format == 0:
        assert number_of_tracks == 1, 'Format 0 files should only have a single track'
    division = int.from_bytes(file_handler.read(2), byteorder='big')
    division_type = (division & 1<<15)
    assert division_type in [0, 1], 'File contains an invalid division in the header'
    delta_time = 0
    if division_type == 0:
        delta_time = (division & (1<<14) - 1)
    else:
        raise TypeError('SMTPE delta times not yet supported')
    return {'format' : format, 'number_of_tracks': number_of_tracks, 'delta_time': delta_time}


def main(file_path):
    """TODO: Docstring for main.

    :file_path: TODO
    :returns: TODO

    """
    count = 0
    with open(file_path, "rb") as file_handler:
        header = parse_header(file_handler)
        print(header)
        track = parse_track(file_handler)


if __name__ == "__main__":
    file = '/media/mark/Data/music/lmd_full/0/00000ec8a66b6bd2ef809b0443eeae41.mid'
    main(file)
