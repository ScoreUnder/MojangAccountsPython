#!/usr/bin/env python3
import mojang_accounts

repo = mojang_accounts.HttpProfileRepository()
# friends 4 lyf?
print(list(repo.find_profiles_by_names("Score_Under", "coldguy101", "foodyling", "combatmedic02")))
