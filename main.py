#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ipfsapi
import sys
import time
from threading import Thread


data = [
    "Hello",
    "IPFS",
    "World!",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam lobortis sapien eros, eget tempus augue auctor sed. Fusce euismod, magna vitae congue pulvinar, odio tellus volutpat orci, nec lacinia nisl lacus quis sem. Ut ligula turpis, vehicula a condimentum auctor, dapibus sit amet ipsum. Aenean iaculis rhoncus metus ut rutrum. Fusce ut turpis eget velit viverra tempor. Phasellus vulputate vestibulum dolor consectetur tincidunt. Sed aliquet dui ut libero placerat, lacinia facilisis sapien dictum. Aenean vel mi eget nisl ornare auctor imperdiet ut ex. Ut et erat ac dolor tempus porttitor. Nulla tincidunt accumsan lacus, sit amet bibendum dolor viverra eu. Praesent id ultrices justo, vitae porta libero. Sed eget aliquam ante, eu bibendum erat. Donec volutpat fermentum lectus vitae dapibus. Vestibulum porttitor ipsum ipsum, ut tempus nisi iaculis eget. Nulla ullamcorper nibh in turpis dignissim, id elementum libero commodo. Fusce condimentum libero quis eros aliquam, hendrerit malesuada augue maximus. Aliquam erat volutpat. Aenean nisi nunc, aliquet vitae eros vestibulum, condimentum volutpat ligula. Phasellus semper porttitor nibh, ut euismod ligula vehicula rhoncus. Phasellus venenatis augue a quam viverra, quis aliquet lacus malesuada. Phasellus pellentesque nisi ut augue ornare placerat. Aliquam ornare vel velit quis rhoncus. Vivamus ac risus mi. Nunc condimentum odio in ex dapibus, non vulputate velit tempor. Nam accumsan vehicula ipsum. Aenean laoreet lorem ut mi pulvinar porttitor. Phasellus non ante sed libero volutpat iaculis. Proin eu feugiat elit, ut vehicula nisi. Aliquam pulvinar tellus at nulla vehicula blandit. Mauris tincidunt dolor sed lorem aliquet tristique. Quisque iaculis erat fringilla sodales pretium. Aenean eget sapien et velit volutpat hendrerit et nec massa. Nulla facilisi. Etiam vitae orci in orci sodales semper in vitae orci. Proin venenatis purus hendrerit venenatis dignissim. Donec tempor augue sit amet enim sodales vestibulum. In non ex lacinia sem consequat sagittis. Maecenas fermentum ultricies vulputate. Sed nec leo eget massa condimentum imperdiet. Nulla facilisi. Fusce auctor elit mi, sit amet rutrum justo vulputate non. Maecenas eu sollicitudin mi. Praesent mattis ex neque, quis tempor dui faucibus eget. Sed tempor, libero ut ornare aliquam, erat eros dictum dolor, vitae fringilla dui metus et mauris. Etiam vehicula nisl libero, et tincidunt dolor bibendum a. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Nam quis auctor metus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Vivamus eget hendrerit purus. Duis ullamcorper mi at metus sollicitudin pulvinar. Integer et eleifend turpis. Suspendisse placerat turpis ante, vel cursus neque sodales et. Vivamus at egestas nibh, nec euismod magna. Praesent ut laoreet arcu. Pellentesque dictum et turpis et fermentum. Nulla sollicitudin nulla at posuere molestie. Aenean luctus ante a convallis vulputate. Vivamus vitae ligula volutpat, fermentum ante nec, tempus lectus. Curabitur vitae est eu mi ultricies maximus. Duis elementum magna quis lacus auctor congue. Sed a purus tempus, accumsan mauris sed, mollis enim. Nulla commodo finibus ante ut rhoncus.",
    "Bacon ipsum dolor amet jerky turkey porchetta, boudin ham strip steak salami ribeye picanha. Strip steak short ribs buffalo porchetta, spare ribs alcatra ham hock tail tongue burgdoggen prosciutto beef tri-tip kevin. Shoulder bresaola pork loin beef pork chop chicken. Pancetta shankle capicola pork loin flank pork belly tail turkey. Turducken pork bacon buffalo. Pastrami frankfurter capicola porchetta ground round. Shankle bacon jerky filet mignon swine. Bresaola shankle rump shoulder bacon meatloaf, flank pancetta sirloin ground round tenderloin pastrami beef t-bone alcatra. Ribeye pork loin kevin kielbasa cupim. Cupim flank sausage strip steak, turkey ham venison. Doner fatback picanha, bacon buffalo t-bone kielbasa cow. Filet mignon shoulder jowl ribeye, t-bone corned beef pastrami rump cupim pig. Pork loin pastrami bresaola tongue, ball tip shankle picanha filet mignon leberkas strip steak pork belly tenderloin tri-tip spare ribs swine. Porchetta bacon pastrami, chicken brisket short ribs frankfurter tri-tip tenderloin pig beef ribs. Rump picanha meatloaf ball tip brisket, salami pork loin turducken cupim burgdoggen chicken short ribs ground round pork. Porchetta buffalo spare ribs pig beef ribs meatloaf corned beef shank tongue salami. Pork chop kevin cow ham hock corned beef. Biltong pork belly landjaeger picanha tri-tip swine prosciutto sirloin chuck andouille strip steak shank burgdoggen filet mignon. Kevin boudin spare ribs, sirloin flank pork chop ground round porchetta ball tip alcatra cupim. Turkey cow filet mignon, hamburger buffalo andouille strip steak porchetta pork chop. Tenderloin turkey rump, shoulder turducken sausage cupim pancetta bresaola. Pig sirloin corned beef, pancetta prosciutto andouille beef ribs burgdoggen hamburger ground round capicola tongue filet mignon. Frankfurter picanha boudin bacon fatback ground round rump sausage spare ribs strip steak. Drumstick shank frankfurter pork loin bacon buffalo sirloin burgdoggen. Tenderloin frankfurter biltong landjaeger, shank pork venison pancetta. Turducken kevin salami tail, shankle pork shank pastrami sirloin pork loin boudin short loin doner swine. Ham hock ham shank, rump tri-tip shankle salami venison short ribs. Rump cupim sirloin swine tenderloin shoulder pork pork loin porchetta. Tenderloin burgdoggen beef pig cupim corned beef jowl kevin salami."
]

IPFSAPI = ipfsapi.Client()
BEGINTIME = time.time()

digests = []
results = []


def reset():
    global BEGINTIME, results
    BEGINTIME = time.time()
    results = [None] * len(data)


def load_into_ipfs():
    for idx in range(len(data)):
        start = time.time() - BEGINTIME
        digests.append(IPFSAPI.add_bytes(bytearray(data[idx], "utf-8")))
        end = time.time() - BEGINTIME
        elapsed = end - start
        print("{: <5}  {:.10f}  {:.10f}  {:.10f}".format(idx, start, end, elapsed))


def load_from_ipfs(idx):
    start = time.time() - BEGINTIME
    results[idx] = IPFSAPI.cat(digests[idx])
    end = time.time() - BEGINTIME
    elapsed = end - start
    print("{: <5}  {:.10f}  {:.10f}  {:.10f}".format(idx, start, end, elapsed))


def fetch_sequential():
    for idx in range(len(data)):
        load_from_ipfs(idx)


def fetch_threaded():
    threads = []
    for idx in range(len(data)):
        threads.append(Thread(target=load_from_ipfs, args=(idx,)))
    for th in threads:
        th.start()
    for th in threads:
        th.join()


def run(attempts=1):
    sequential_time = threaded_time = 0

    reset()
    print("")
    print("======= Sequential Push (Just Once) =======")
    print("Index  Start         End           Elapsed")
    start = time.time()
    load_into_ipfs()
    elapsed = time.time() - start
    print("Total {} items pushed to IPFS sequentially in {} seconds".format(len(data), elapsed))

    for attempt in range(attempts):
        reset()
        print("")
        print("======= Sequential Fetch (Attempt #{}) =======".format(attempt))
        print("Index  Start         End           Elapsed")
        start = time.time()
        fetch_sequential()
        elapsed = time.time() - start
        sequential_time += elapsed
        print("Total {} items fetched from IPFS sequentially in {} seconds".format(len(data), elapsed))

    for attempt in range(attempts):
        reset()
        print("")
        print("======= Threaded Fetch (Attempt #{}) =======".format(attempt))
        print("Index  Start         End           Elapsed")
        start = time.time()
        fetch_threaded()
        elapsed = time.time() - start
        threaded_time += elapsed
        print("Total {} items fetched from IPFS concurrently in {} seconds".format(len(data), elapsed))

    print("")
    print("======= SUMMARY =======")
    print("Data Items:      {}".format(len(data)))
    print("Fetch Attempts:  {}".format(attempts))
    print("Mean Fetch Time (Sequential):  {:.10f} seconds/item".format(sequential_time/attempts/len(data)))
    print("Mean Fetch Time (Threaded):    {:.10f} seconds/item".format(threaded_time/attempts/len(data)))


def print_help():
    print("Usage:   {} [<max-items> [<attempts>]]".format(__file__))
    print("<max-items> : Number of items from the data to be used (Default: {})".format(len(data)))
    print("<attempts>  : Number of iterations to perform fetches  (Default: 3)")
    sys.exit()


if __name__ == "__main__":
    attempts = 3
    if set(["-h", "--help"]) & set(sys.argv[1:]):
        print_help()
    try:
        if len(sys.argv) > 2:
            attempts = int(sys.argv[2])
        if len(sys.argv) > 1:
            del data[int(sys.argv[1]):]
    except Exception as e:
        print(e)
        print("")
        print_help()
    run(attempts)
