def generate_rodada(copa):
    from get_matches import get_matches
    from send_email import send_email
    tiers = "tiers.txt"
    matches = get_matches(tiers, copa)
    addresses = 'addresses.txt'
    send_email(matches, addresses, "bolão FñA - testando o robô")


if __name__ == '__main__':
    copa = False
    generate_rodada(copa)
