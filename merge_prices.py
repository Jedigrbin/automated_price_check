# =========================
# LOAD NEW PRICES
# =========================

new_prices = {}

with open("new_prices.txt") as f:
    for line in f:
        parts = line.strip().split("\t")

        if len(parts) == 2:
            code, new_price = parts
            new_prices[code.strip()] = new_price.strip()

# =========================
# MERGE WITH PRODUCTS FILE
# =========================

with open("products.txt") as f, open("results.txt", "w") as out:

    # Optional: header (you can remove if not needed)
    out.write("CODE\tNAME\tOLD_PRICE\tNEW_PRICE\tCHANGE\n")

    for line in f:
        parts = line.strip().split("\t")

        if len(parts) == 3:
            code, name, old_price = parts

            code = code.strip()
            name = name.strip()
            old_price = old_price.strip()

            # match using code
            new_price = new_prices.get(code, "NOT_FOUND")

            # CHANGE LOGIC
            change = "N" if old_price.strip() == new_price.strip() else "Y"

            out.write(f"{code}\t{name}\t{old_price}\t{new_price}\t{change}\n")

print("Done → results.txt created")
