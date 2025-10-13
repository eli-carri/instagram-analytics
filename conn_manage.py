import pandas as pd
from colorama import init, Style, Fore
from conn_unzip import find_file

def imp_followers (followers_file):
    followers = pd.read_json(followers_file)
    followers = followers.string_list_data
    for i in range(len(followers)):
        followers[i] = followers[i][0]['value']

    followers = pd.Series(followers, name="followers")
    return followers

def imp_following (following_file):
    following = pd.read_json(following_file)
    following = following.relationships_following
    for i in range(len(following)):
        following[i] = following[i]['title']

    following = pd.Series(following, name="following")
    return following

def read_txt(name):
    # read file
    file = open(name, "r")
    text = file.read()
    lines = text.split("\n")
    lines.remove("") 
    file.close()

    # return lines
    return pd.Series(lines)

def to_txt (list, name):
    # create/replace file
    file = open(name, "w")
    for line in list:
        file.write(line + "\n")

    # close file
    file.close()


def check_following ():
    # import following users
    fwing = imp_following("connections/followers_and_following/following.json")

    if find_file("^users_following.txt$") is None:
        print("No old following file.")
    
    else: 
        # get new following users
        old_fwing = read_txt("users_following.txt")
        new_fwing = fwing[~fwing.isin(old_fwing)]

        # get unfollowing users
        unfwing = old_fwing[~old_fwing.isin(fwing)]

        # show number of following users
        init(autoreset=True)
        dif = fwing.size - old_fwing.size
        COLOR = Fore.GREEN 
        if dif < 0:
            COLOR = Fore.RED
        print ("> Following: " + Style.BRIGHT + f"{fwing.size} " + Style.RESET_ALL + COLOR + f"({dif})")

        print("\n-------- FOLLOWING USERS INFO --------")
        # show unfollowed users
        if not unfwing.empty:
            print("> Unfollowed users:")
            for user in unfwing:
                init(autoreset=True)
                print("  - " + Style.BRIGHT + user)            

        # show new following users
        if new_fwing.empty:
            init(autoreset=True)
            print("> New following users up-to-date!")

        else:
            print ("> New following:")
            for user in new_fwing:
                init(autoreset=True)
                print("  - " + Style.BRIGHT + user)
            
        # show old following users
        old_fwing_list = old_fwing.to_list()
        print (f"> Last {min(5, len(old_fwing_list))} old following users:")
        for u in range(min(5, len(old_fwing_list))):
            init(autoreset=True)
            print("  - " + Style.BRIGHT + old_fwing_list[u])
        
    # save following users list    
    try:
        to_txt(fwing, "users_following.txt")
        init(autoreset=True)
        print(Fore.GREEN + "\nFollowing users saved succesfully!\n")
    
    except:
        init(autoreset=True)
        print(Fore.RED + "\nUps! Can't save following users.\n")

def check_followers ():
    # import followers
    fwers = imp_followers("connections/followers_and_following/followers_1.json")
    fwing = imp_following("connections/followers_and_following/following.json")

    if find_file("^users_followers.txt$") is None:
        print("No old followers file.")

        unfwers = fwing[~fwing.isin(fwers)]
        to_txt(unfwers, "users_unfollowers.txt")
    
    else:
        # get new followers
        old_fwers = read_txt("users_followers.txt")
        new_fwers = fwers[~fwers.isin(old_fwers)]

        # get unfollowers
        unfwers = old_fwers[~old_fwers.isin(fwers)]

        # get new unfollowers
        old_unfwers = read_txt("users_unfollowers.txt")
        new_unfwers = unfwers[~unfwers.isin(old_unfwers)].copy()

        # show number of followers
        init(autoreset=True)
        dif = fwers.size - old_fwers.size
        COLOR = Fore.GREEN 
        if dif < 0:
            COLOR = Fore.RED
        print ("> Followers: " + Style.BRIGHT + f"{fwers.size} " + Style.RESET_ALL + COLOR + f"({dif})")

        # show new followers
        print("\n-------- FOLLOWERS USERS INFO --------")
        if new_fwers.empty:
            init(autoreset=True)
            print ("> New followers up-to-date!")

        else:
            print ("> New followers:")
            for user in new_fwers:
                init(autoreset=True)
                print("  - " + Style.BRIGHT + user)

        # show old followers
        old_fwers_list = old_fwers.to_list()
        print (f"> Last {min(5, len(old_fwers_list))} old followers:")
        for u in range(min(5, len(old_fwers_list))):
            init(autoreset=True)
            print("  - " + Style.BRIGHT + old_fwers_list[u])

        # show new unfollowers info
        print("\n------- UNFOLLOWERS USERS INFO -------")
        if new_unfwers.empty:
            print("> New unfollowers up-to-date!")

        else:
            new_unfwers_df = pd.DataFrame({"new_unfollowers":new_unfwers, "following": new_unfwers.isin(fwing)})
            print("> New unfollowers:")
            for row in range (new_unfwers.size):
                # User + Info
                user = new_unfwers_df["new_unfollowers"].iloc[row]
                following = new_unfwers_df["following"].iloc[row]
                
                # Divide the cases
                init(autoreset=True)
                if following:
                    print("  - " + Style.BRIGHT + f"{user}" + Style.RESET_ALL + " - " + Fore.RED + "Following")

                else:
                    print("  - " + Style.BRIGHT + f"{user}" + Style.RESET_ALL + " - " + Fore.GREEN + "Not following")

        # show old unfollowers info
        old_unfwers_df = pd.DataFrame({"old_unfollowers":old_unfwers, "following": old_unfwers.isin(fwing)})
        print(f"> Last {min(5, old_unfwers_df.shape[0])} old unfollowers:")
        for row in range (min(5, len(old_unfwers))):
            # User + Info
            user = old_unfwers_df["old_unfollowers"].iloc[row]
            following = old_unfwers_df["following"].iloc[row]
            
            # Divide the cases
            init(autoreset=True)
            if following:
                print("  - " + Style.BRIGHT + f"{user}" + Style.RESET_ALL + " - " + Fore.RED + "Following")

            else:
                print("  - " + Style.BRIGHT + f"{user}" + Style.RESET_ALL + " - " + Fore.GREEN + "Not following")

        # save unfollowers
        try:
            to_txt(unfwers, "users_unfollowers.txt")
            init(autoreset=True)
            print(Fore.GREEN + "\nUnfollowers saved succesfully!")

        except:
            init(autoreset=True)
            print(Fore.RED + "\nUps! Can't save unfollowers.")

    # save followers
    try:
        to_txt(fwers, "users_followers.txt")
        init(autoreset=True)
        print(Fore.GREEN + "Followers saved succesfully!")
        
    except:
        init(autoreset=True)
        print(Fore.RED + "Ups! Can't save followers.")

if __name__ == '__main__':
    check_followers()
    check_following()