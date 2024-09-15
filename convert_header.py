from email.header import decode_header

# the file ./mail_header.txt contains a copy of the To: header of an email (only the value)
# e.g. Name <name@domain.com>, Name2 <name2@domain2.com>

# objective: extract the Names and the email adresses to a csv file emails.csv

def decode_decoded_part(part: tuple[bytes, str]) -> str:
    """
    Decodes a part of the header.
    """
    data, charset = part
    if charset is None:
        return data.decode("ascii") # no charset, decode with ascii
    if charset.lower() == 'utf-8':
        return data.decode('utf-8') # utf-8 specified, decode with utf-8

def read_file(file) -> str:
    """
    Reads the file and returns the content as a string. Decodes the header.
    """
    with open(file, 'r') as f:
        return " ".join([decode_decoded_part(part) for part in decode_header(f.read())])
    
def extract_emails(content: str) -> list[(str, str)]:
    """
    Extracts the names and emails from the content.
    """
    emails = []
    for line in content.split(','):
        name, email = line.split('<')
        emails.append((name.strip().replace("  ", " "), email.strip().replace('>', '').replace("  ", " ")))
    return emails

def write_csv(emails: list[(str, str)], file: str):
    """
    Writes the emails to a csv file.
    """
    with open(file, 'w', -1, "utf-8") as f:
        f.write('Name\tEmail\n')
        for name, email in emails:
            f.write(f'{name}\t{email}\n')
        f.close()

if __name__ == "__main__":
    content = read_file('./mail_header.txt')
    emails = extract_emails(content)
    write_csv(emails, 'emails.csv')