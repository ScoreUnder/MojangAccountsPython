#!/usr/bin/env python3
# Run with "python3 -i" for more fun
import mojang_accounts

repo = mojang_accounts.HttpProfileRepository()
# friends 4 lyf?
people = list(repo.find_profiles_by_names("Score_Under", "coldguy101", "foodyling", "combatmedic02", "DenkouKonishi"))
print("Some people: %s" % people)
