class CustomCsvReader:
    """
    Stream CSV reader implemented as an iterator.
    Yields one row at a time as a list of strings.
    """

    def __init__(self, file_obj, delimiter=",", quotechar='"'):
        self.file_obj = file_obj
        self.delimiter = delimiter
        self.quotechar = quotechar

    def __iter__(self):
        return self

    def __next__(self):
        buffer = []
        fields = []
        in_quotes = False

        while True:
            ch = self.file_obj.read(1)

            # End of file
            if ch == "":
                # Return last row if there is buffered data
                if in_quotes:
                    # Unterminated quoted field: treat as data
                    fields.append("".join(buffer))
                    return fields
                if buffer or fields:
                    fields.append("".join(buffer))
                    return fields
                raise StopIteration

            # Handle quote characters
            if ch == self.quotechar:
                if not in_quotes:
                    # Enter quoted field
                    in_quotes = True
                else:
                    # Possible escaped quote
                    next_ch = self.file_obj.read(1)
                    if next_ch == self.quotechar:
                        buffer.append(self.quotechar)
                    else:
                        # End of quoted field; push back char by manually handling it
                        in_quotes = False
                        if next_ch == "":
                            # EOF after quote
                            fields.append("".join(buffer))
                            return fields
                        if next_ch == self.delimiter:
                            fields.append("".join(buffer))
                            buffer = []
                        elif next_ch == "\n":
                            fields.append("".join(buffer))
                            return fields
                        else:
                            buffer.append(next_ch)
                continue

            if in_quotes:
                # Inside quotes everything is literal (including delimiter and newline)
                buffer.append(ch)
                continue

            # Not in quotes: delimiter or newline ends field/row
            if ch == self.delimiter:
                fields.append("".join(buffer))
                buffer = []
                continue

            if ch == "\n":
                fields.append("".join(buffer))
                return fields

            # Normal character
            buffer.append(ch)


class CustomCsvWriter:
    """
    Simple CSV writer.
    """

    def __init__(self, file_obj, delimiter=",", quotechar='"'):
        self.file_obj = file_obj
        self.delimiter = delimiter
        self.quotechar = quotechar

    def _needs_quotes(self, value: str) -> bool:
        return (
            self.delimiter in value
            or self.quotechar in value
            or "\n" in value
            or "\r" in value
        )

    def _escape_field(self, value) -> str:
        if value is None:
            value = ""
        value = str(value)
        if self._needs_quotes(value):
            # Escape existing quotes by doubling them
            escaped = value.replace(self.quotechar, self.quotechar * 2)
            return f'{self.quotechar}{escaped}{self.quotechar}'
        return value

    def writerow(self, row):
        escaped_fields = [self._escape_field(f) for f in row]
        line = self.delimiter.join(escaped_fields) + "\n"
        self.file_obj.write(line)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
