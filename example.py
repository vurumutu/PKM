# -*- coding: utf-8 -*-

from xpressnet import Client
from xpressnet import Train
from time import sleep

TCP_IP = '192.168.210.200'
TCP_PORT = 5550


def menu():
    print("1. Do przodu - max prędkość")
    print("2. Do tylu - max prędkość")
    print("3. Do przodu - ustal prędkość")
    print("4. Do tylu - ustal prędkość")
    print("5. Stop - zerowa prędkość")
    print("6. Wyłącz zasilanie pociągów")  # klawisz off na pilocie
    print("0. Zakończ")
    print("Aby zakończyć program naciśnij klawisz q.")


def main():
    direction = {"Forward": 1, "Backward": 0}
    client = Client()
    client.connect(TCP_IP, TCP_PORT)
    while True:
        numer = input("Podaj numer pociągu[1-7]: ")
        if numer not in range(1, 8):
            print("Nieprawidłowy numer pociągu.\n")
            continue
        train = Train(numer)
        while True:
            key = input(menu())
            if key == 1:
                msg = train.move(127, direction["Forward"])  # do przodu z prędkością max
            elif key == 2:
                msg = train.move(127, direction["Backward"])  # do tylu z prędkością max
            elif key == 3:
                vel = input("Zakres[0-127]: ")
                msg = train.move(vel, direction["Forward"])  # do przodu z określoną prędkością
            elif key == 4:
                vel = input("Zakres[0-127]: ")
                msg = train.move(vel, direction["Backward"])  # do tylu z określoną prędkością
            elif key == 5:
                msg = train.move(0)  # Stop - zadanie zerowej prędkości
            elif key == 6:
                msg = client.stop_all_locomotives()  # Zatrzymanie wszystkich lokomotyw awaryjnie
            elif key == 7:
                msg = train.stop_locomotive()  # Zatrzymanie aktualnej lokomotywy awaryjnie
            elif key == 0:
                msg = train.move(0)  # Zakończ
                client.send(msg)
                sleep(1)
                break
            else:
                print("Podano nieprawidłowy klawisz!")
                continue
            client.send(msg)
            sleep(1)  # Czekaj 1s
        key1 = raw_input(menu())
        if key1 == 'q' or key1 == 'Q':
            break
        else:
            continue
    client.disconnect()

if __name__ == "__main__":
    main()

# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNMMMMNMMMMMMMMMMMMMMNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNMMNMNmdhysosoooo+++++osssyhdmNNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNmho/-..``````..:+++/:::.``..--/ohmMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMNMMMMh+-`````..```-/.---:---:-.``..``.-omNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMNd/.`.-.``-..``.-..` /.`-`.-`...````-ymMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMNNmo..`.:-.....```.-.` -.-/....----.--.odNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMd:``` .``````````.````````````````..-/yNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMms-.``````..`.....-://:-.....````````+hNNMMNMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMNMMNs/-.`````````````.......`````````.omNMNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMNm/.` ```````````````.``````````````-hNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMNm+-.````````....---:/:::-..````` `./dNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNdo-  ````...--:://+o++/::-..``` .:hNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMh/.-:/+ossyyyhhhdddddhhhhyysso+/:/hNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN+-:yysoo+++///+//+oo++oso++++oossshNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMNN/-:s.` ```....-/:/+o/+yh+:..````-/yNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMNN/:/y. `-syhh:/ymoodyoodNmh/ho/+.`-ymNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMNm//+s` `/mdyMoohNoomh+/+mds.hmmh.`.sdNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMNm//++` `/mh/NysyNoodh+/ymo-.odmo` `+dNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMNm:+o:` `:mdsNsosNyymyoommy/.:ym:` `+hmMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMNd:os.  `:ddhh:-:hddh/+sdhdy--sh-` `:ymMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMNy-oy`   `::-....-::://:::--.`-:.`  .ohNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMmo-oy``   ``..---://+o++++///:::-----ohNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMm+:+o` .-:/osyhdmNmNNNNNNNNmNmmmmmmmdmmmMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMMNd:/++-+yddmmmmmmNNhysmmhssssssydNhso+oymMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMMNy-/oyyoyhymy/.:sNm/-.mmy..://..:mo:.::omMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMMms.+yh+.`.omy- :sMN/..NNy.-ohd-`-ds:.y/odNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMNMMMNds:yo/-``-dNy- :yMN/..MNh-.://`-+Ny:`--+dmNMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMNyo+yo/s.:sNMy: :yMN/..NNy.-+sh/--sy/`+:+ymNNMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMNs+oyhy:.oNdmy: -sNh:..MNy.-+sy:..+y/.yoosmNMNMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMmo/ymds`+yy:dho..-/--/oNmh+++++/+sdhsohdhyymMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMd+/dNs-`/:::dmmyysyyyhddddddhhhysoyyyyso+/omMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMy//Nh/./oyhdhyso+osshhyhhhddhyoooo+:.```.-ymNMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMNMMMs:/Nyyyyso/::/++osoyyyyyyhyyysso+/:.`````-ydNMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMNo/oNhs+-``.`.-//::::::///////::-.`.``````.shmMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMN/+sy:.```````...-:-://:o+/:::::.--```````.sydMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMNd:++.``````````-sys/hhyommy:ooo+/oo.``````.osdMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMNd:-.``````````./NdyoNdhhddy/ddmmddy.```````/sdNMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMNh-..-`````````.:Ndysmdhymdy/dhhdddy.```````.shmMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMNNms./oo.```````..-oo+:so+:so+:ooo+oo+-````````ohmMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMNdo`/sddy+-````..-----::::+////::::-..-.```.-yyhhNMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMNMNh/``.:shmd/-`.-----::///://///////:-.--.`-+dh//sMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMmy:.```.-/ydho-.--:::::://+++++////:---../hho-.:oMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMds:....`.../oys/:--:/+o+oooo+oooo++/:--/oy+:.`.:oNMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMdo:....-...`..-/++/--:/++ooooooo+/::::+/:...`.-:/NNMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMho-.--.----......------::://////:::::-.....-----:mNMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMNy+-..-.------..---.------:::::::::--------------:dNMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMms/...--------------::::://////////::::---------::ymMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMms/...--------------::::////+++/++///:-----------:odNMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMms:...-------------:::::::-:/+///+///:------------+dNMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMdo:....-------------:::/:-.://///////::----------:+dNMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMh+:....-------------:::/:-.-/////////::----------:/hNMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMy/-.----------------:::/:-.-://://///::-----------:yNMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMs/--.---------------:::/:-.-://://///::-----------:ymMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMs/--.----------------::/:-.-::/::////::------------sdMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMNo:--.---------------:::::-.-::/::///:::------------odMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMo:-...--------------:::::-..::/:::///::------------odMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMo:-...--------------:::::-..::/::://:::------------ohMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMo:-...---------------::::-.-:::::://:::------------ohMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMo:-..------------------::-.-:::::://:::------------+hMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMo:-..------------------::-.-:::::://:::------------+hMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMNo:-...------..--------:::-.-:::::://::-------------+hMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMo:-...-------.---------::-.-::::-:/:::-------------+hMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMo:-.---------..--------::-.-::::::/:::-------------+hMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMNo:-.---------..--------:--..::/:::/:::-------------+yMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMN+:-.--------...-----:::/::-://////+///:------------/sNMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMNm/:----------...-----:::+///+oo++++o+//:-----------.:omMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMmh/-----------------:::://:::oyy+://o+//:----------..-+hNMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMNdy-.`....-----..-----::::---:sdho:--:/::------.....``.-+NMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMdyo.```````````````...---.`..-://:.``..````````````````.:hmMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMNms+/``````````````.........................```````````.`../ymNMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMNMNmo+//.``........----------.---..---.---.---.....--.........-/sdNMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMNNMNho/++/--------------------------------------------------------:odmNMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMNNNms+/o++/--------------------------------------------------:::----:+shNMMMMMMMMMMMMMMM
# MMMMMMMMMMMMNmh+++o+/:---------------------------------------------------:::------/+sdNMMMMMMMMMMMMM
# MMMMMMMMMMNNhs++++/------------------------------------------------------:::::::---::+ydNMMMMMMMMMMM
# MMMMMMMMMNmyo+++:::----------------------------------------------------::::--::::---::/ohmNMMMMMMMMM
# MMMMMMMMNds++//:---------------------------------------------:--:-------:::::::::::--:-:+ydNMMMMMMMM
# MMMMMMNNhs++/::---------------------------------..-----------::::::-------:::::::::--::::/odNNMMMMMM
# MMMMNNNhoo+/---:------------------------:::-......--------.---:--:::------:::::::::::-::--:+dNMMMMMM
# MMMMNmhso/:----------------------------::::-......:---:--:-------::-------::-::::::::-::::::odNMMMMM
# MMMMNho+/:::------------------------:::::::::-....-:/sy+::-..--://::-----::::::::::::::-::::-ohNMMMM
# NMMNhs+/::::------------------------::::::///-....-:+dds/:..--:/++//:-------::::::::::::::::-:odMMMM
# NMNmo+/::--------------------------:::::::////....--+mso/-..-:+oo+++/::-----::::::::::::::::-:/+NNMM
# MMNyo/::--------------------------::--:::://++:-..--:o//:...-+oooo++//::----:::::::::::::::::::/dNMM
# MNdo+:--::------------------..----:---:::::/++o/--:::////:-:/ssso++////:-----:::::::::::::::::::omMM
# Mmyo/::-:-------------------..---------:::://+s+//+oossoo++//oooo+/////::------::::::::::::::::-/hNM
# Mhs+:::-:-----------------....-----------:::/++++++oooooo++++ooo++///::::----------::::::::::::::smM
# Nyo+:::-----------------......-----------::::/:::-..-++o++/++/+++////::::-------------::::::::::-ohM
# myo/:--:---------------......-------------::://:-```.:///://::///////::::---------------::::::::-+yN
# myo:-------------------.....---------------:::/:-``..-::::/::-://////::::---------------::::::::-/yN
# my+:-------------------.....---------------::--..````..-::::---:/:::::------------------:-::::::-/sN
# ds+:-------------------......--....--------:-.````.```..--:--..-:----.------------------:-::::::-/sm
# ds+:-------------------.....---....-..-------`.```````.---.--.........-------------------:::::::-/sm
# ms/:-----------------........--.....--------.`.```````.....---......----------------------::::::-/sm
# ms+:-----------------.........--.......----..```````.......--------------------------------:::::-/sN
# my+:-----------------.........---.......---.````..``.......----------------------------------:::-/sN
# Ny+:-------------..--...................---..``....`.......---........---------------------------/sN
# Ny+/------------...--........................`````````................------..-------------------/sN
# Ny+/-----------.....-..........................----::-::::----.........---...--..----------------/sN
# Ny+:-------............-...-.`...-/++/://::/++ooooooooosssssso++/:--........-..--.---------------/yN
# Ny+:--------........-....``....///+oo++oo++oo+::::-----::/::/++oossso+/:-.......`...-------------/yN
# Ny+/-------.-.........`````.-:+:///:/++++/ooosoo+/------:-::::--:::/+oooo/////:.`....------------/yN
# Ny+/---------......````.-:+so++:/++///+oo++oooosssyo/--+s+/++:++/--::--:/+oo++ooo:.``...---------/yN
# Ny+/---------.....```.:syyhyssso++//+ossssooooosyyyhhs//+s+ss/+o+//++:---::/+++//ss+.``..--------/yN
# Nyo/--------....```:oyyyyyyhyyyyso/-/oyssyssssosssyyhdyo+/:::::/+++sy:++-:--:://+:+oy:.`...------/yN
# Nyo/-------....``-+dhyo+ossyssssso+/ohyosyssssossyyyyhhyyys+/---:::/+/so+///:--:/::/sho:`.......-/yN
# Nyo:---....````.oyhsys+-/+o+oo+/:--:/++ssshsssosssyyssyyyyhhhso+//::--/++:oo+/::-:::-oyho-.`.``.-/yN
# Ny+:-...`````-:shyoso+:-:::::-.---````.:/+yooooossysssyyyshhddhyhhys+:---:+++o+:----:-/sds/-`...-/sN
# Ny+:....`..-oyhdo/:o/:-o+/-...-o+/````.-:://+oossssssssssshhhdhhhhddds:----:+///+:---:-:sdhy/:-.-/sm
# Ny+:-:://osyhhhs------.oo+/--:+s+:.````.-:+oossyssoososssosyhhhyyddhhd/-----::/+so/-.---:yhhhyso++yN
# Ny+-oyhhhhhyhys----...-oss+---:/:.````.:/+oossyooo++ooooosossyyyyyhhhho/-----::/+oo/-.--.+shhhyyhoym
# Nh+-oyhyhyyso/-....-::-sso/-...-.....`.///+ooooooo+++/:/+oooossssshhhyyyy:--:---:+++/-....:osyyyyoyN
# Nh+-oyy+/:-.```-..-/so/+yys+/-....:.``.---/+oo+ooo++/-.-:++++sso++ssyhsymds+:----:/+o/-......-:/ysym
# Mho-oys.`````...`-+oo/-:oss/++/--::````..-:+oooooo++/-`.-////+++/:+osyyhdNmds/-----/oo/-.......-ssym
# Mdo-oyy..````...-/oo/-.-::....-./+-`````..:/++so+++/:.```.---:::-.:+oydmdmNNNy+:----/+o+...-...-/+ym
# Mds-oyy-.```....oso/-.../++....:/:.``````.-/++sooo//-.`````.....`.-/++hmmydNNNds:---.:+s:..-...--/sm
# Mdo.+yy:.``..`.+ys/....-/oy++o+/-.`---```.-/++oooo+/:.``  `..`::-`.-::ydm+hmNNNmy:----:++:.....--+ym
# Mds-oyy-`````.--/:-..../oymyyyy+-`.+oo+:-../+ossoo//:.````````oyy-...:shh+ydNNNNmo/-..:+o/-.....:shm
# Mms-oyy:`````.:o:.`..-:ohmNNNNNm+.`:/+s+/-./osso++::--.-:/.```sdNd/-.-+smyyhmNNNNds/----+/-....-shdm
# Mms-+yy:````.:oo-.`.-:/dNNMNNNNNy/``.-///:.+sso+//:-/shdmm/.`.ymMNdo:.:omNNNNNMMNNds:-..-..`..:omddm
# Mms:+yy:````-/o+....:+yNNNNNNNNNmy-```.ooo/osys+/::+yNNNNNs:-/dNNMNds.-oNNNNNNNNNMNd+-..````-+ymNhhm
# Mds:+yy:````/++:.`.:/smNNNNmNNNNNd/.`.+dmNmdhso/:-+hmNNNNmo+/dNMMNNNd-/yNNNNNNNNNNmh+-....:+ydmNNhhd
# Mms:+yy:```.++/`.../shNNNNNNNNNNNmo--/mNMNNNhs+/::hmMNNNmy+oyNNNNNNNm/ohMNNmmhhys/:-.--:+sydmNNmNhhd
# Mds:+yy:```-++/...:+hNMMNNNNNNNMmdo:+yMNNNNNds:-/yNNNNNmho:ohNNNNNmdh++oso+//-----:/+oyhdmNMNNNNNhyh
# Mds:+yy:```:+/:..-/smNNNNNNNNNNNdy+/ymNmmNNNdy-:odmmmdmdho/oyyoo+++os+/::::://+osyyhhdmNNNmmhmmNNhyh
# Mds:+yy:.`.:+:.`-:/ydmdhyyssssymdy/:/+/++//osy:////::-:::----:::/+ydmooosyyyyhhddmNNNNNNddyo/:omNdhd
# Mds:/yy:.``.:-` ...-::------:::sso+:////+++sys://++oooossyyyyhhhhhddhyhdmdmmNNNNNNNNmddho/-`` :yNdhd
# Mmy:+sy/`````.-:/+++oooossssssysyyyyyyhyyhhmdhooshhhhhhhdddmmmmmmmNNNNNMMNMMNNMNNdyss/-.   `.`-oNdhh
# Nmy-/sy:.-:osyyhhddmmmmdmmmmmmmmmmmmmmmmmNNNNmmmNNNNNNNNNNNNNNNNNMNNNNNNNNNNNMNNN+-.`   `..```-oNdhh
# Nmy-/+o/shdmmmmdhhdMNNMNNNNNNNNNNNNNNMNNNNNNNNNNNNNNNNmmNNNNmmddhhyssooooosymNMMMh/`   `-yhy.`:yMdyy
# Mmy::/ohmNNNmhs:-.-sdmmdmmmddddddddhhdNNNmdhyhhyyyoshmyo/:::::--...``     `.-hmNMd+.`  .hNmh.`/dNdyy
# Mmy:-odmmmmmNs-   `.+oo/+yMs:.....``-+mNNmy-`    ``+hMds:          `` `      :hNNmo-   .mmds`:sNNdyy
# Mmy-/ymmdhhhooo+::-  ```odMd+.      +dNMMMN+-     -yNMMdo`  ` `  ..-:.`````` .smMmo-   .hho-.sdNNdhy
# Nmy-ohmmd+`````-.```   +dMNms:      oMMMMNmy/     /dMMMms`   ` .:dNNNNo-`    `smMd+.  ``:.```.+mNdhy
# Mmy-ohmmm+` ```````  `.mNMMms:      oMMMMNmy/     /dMMNmy   `` -+NMMMNy/`    :yNMmo- `  ``````:yNdhy
# MNd/shmmm+``/yds.    -sNMMMmo:      oMMNNMms:     /dMMNmy   `  -+NNmdd/.  ``-hNMMd+-  ``.::-``-oNdhy
# MMd/ohmmm+./mNdo. ` .+mNMMMms:      oMMMMNms:     /dMMNmy`  ` `.:so+/.` ``:odNMMMmo. ` .ymho``-/Ndhy
# MMd/+ymmd+:dmmh.``` +hNNNNMms:      oMMMMNNs:`    /dMMNms   ```````` ``` `..-ydNNmo.   .NNmy``.-dhys
# MMd/+ydddsoNmho    -hNNNNMNms:      oMMMMNNo:     /dMMNmy   `````..---```   ``odMmo. ` .mNmy``:yNsos
# MMd/+yddmddNdo.   `ymNNmNNMms:     `oMMMMNNo-     /dMMNmy `````./mdmmmh+-`    -oMd+.   .mNmh/ydNh+/s
# MMd/+ymdmmmmy:`  .:NNNmdhdMms:     `oMMMMMNo-     /dMMNmy   `` -oNMMMNNy-   ` -sMd+.   .ymNNmNNd/+os
# MNd//ymdmmmd/.  `/hMNmhs+sMds:     `sMMMNNN+-     /dMMNmy `````-+NNNmmh+.``  `+dNd/` `.-smNNNmy/:oss
# MNd+/ymdmmdy.`  :smNdhy.:sMms:     `oMMNNmN/.     +dMMNmy ``````.osso/.` `   +hNms/-/shmNMNmho:.+oss
# MNd//ymmNmh/`   ohmds/. -sMNy/      :sdddho.  `   ymMNmds     ``````` ````.:smNNNhddNNNNmdyo:...+sss
# MNd//ymmmds.`  `/+/:.`  -oNMms`    ```.-..``  ``.:NNNNdy/    `  ` ``.-::+shmNmhhmNNNmmdhs+:-.`..+sss
# MMd+/ymmdy+ `  `       `-oMNNmy/-.` ``   `````-+ydMNNNho/://+osyyyhhddddmddhso+oyhhys+/:....:-.-+sss
# MMd+/ymmd+.  `..---/////+yMNNMNdhyo////////osydNNNMNNNNmdmmmmmmmmmmddhhyysoo++++s+/:-----..-+:--+sss
# MMd+/ymmho:+syhdddmNNNNNmmNmmmmmmdmddddddddhhhhhhhdhhddddhhhhhyyyyssssoooooo+++/::/+oys/:..-+:-.+oss
# MMd+:ymmmddmmmmmddddhhhhhhhhysoooooooooooooossosssyssossoossyysooooooooooooo+o++ohdmNds/..-:+-..+sys
# MNd+:ymmdddhyyyssssoo++++++/////+++++++ooo+syd+osshoodsoooyyhhsoossoooooo+++o++odNNMNy+:..-//-..+sss
# MMmo:ymdyys+/:-......------::///+++++oossss+sdoooso+smoyhsyyyhhyossoooooo++++++smNNNmo/-`.:+:-.-+sso
# MMdo/yds:-`````````.-/+ssssyo//++++++++++++osy+sss/oshsys+yyyssooooooo++ossssydmNNNNy/-..-:+...-+sss
# MMdo/oo-```.``./.`..:+sNmmmms///+++++++oooosssossosssssoossoosoossssyhhhhddddmNNNNNm+:-.---:..../sss
# MMmo/::.-.`.`.:o:..`-:+mmNMmo////+oosssssssyysyyyyyhhhhhhhdddddddmddddmmmmNNNNNNMNmy:-..oys+-..-/sss
# MMmo:---:-....-o+:...-:ydNNds+osyhhhhdhddddddmddmmmmmmmmmmmmmmmmNmmNNNNNNNNNNNNNMNy+-..-+so:..../sss
# MMms:-.`-..`.../o+-..../sdNNmddmmmmNNNmNNNNNNNNNNmmmmdNNNNNNNNNNNNNNNNNNNNNNNNNNNy+---:/s/:.-..-/sys
# MMmo::/-...`..../++....-/smMNNNNNNmdddmmmNNMNNNdyso++++osyhdmNNNNNmmmdddmNNNNNNNd/:-.-/o:/:...../sss
# MMmo-+so-..`....-/o:-...-:omNNNhs++::/+osymdhy//++syyyyyysooshmmdso++++oooydNNNh/:---o+/+--.`--./sss
# MMms-+ys/-````.-..-.::...-:sdmy/+sy+//+yhyoo+/shddo+/:/oydmdhyyo++yys++oyosyhNy+----/sso--.....:osso
# MMms-+shyso:.``...-syo:...-:+o/so+o//++ssoo/ohdhhds/-::oydhhdddys/sso+/+o/osyo/----:o/::--..-+syyyso
# MMms:/oydhhyo/-`.-:so+//--.--:+ys+++//:oo/-ydhsooosso/ossosyyhddh+o++////+yhh.----/+os/.-.-:oyhdysoo
# MMNd:-.-+shdhhy/-.-./oh+:....:syo+/++o+/++ohhho+osooosssso+osddmdo//++++++shd-..-+oo-:--.:ohhdyo:-/o
# MMNd/:-...:ohddh:.--:+y:///..:+yo+++/:o++osssossydoo+++shdyyyoyddy//+++++ohhs---+/oo/--:-syhdo:..-/s
# MMNm+:--....:odhy+.---:o+///:-:so+/+//o+++syhysyyho++s+oyhysyhdddo/os+osshho-.-/h+/:-:--+ddy/--.-:/s
# MMNd+:----....:ydh+.---+++s/+/-:/ohyyysyssohdh/:+hyo+::oyy//odmdh/yyysssyo:-.s+//o/-:--/dh+....--:+s
# MMNd/:------..`.ohd/--::--:+sss:--:+oos+/:oyhd+::shs+/syyo-/smmy+.+oo+//:-:/:ooo+:::--oyy:.`..---:+s
# MMNd+:------..-`./yd+:./::.+yy+/:::-...--.-oyddhys+++++ooyddmms/.------://+os://-::--oyy.`...----:/s
# MMNd+:--------..``.shy/-::/-:/-/os/-:/------:+hdmdddhhddmmdhy/-------::+yyo++:::/:::sy+-`.-------:/s
# MMNd+:----------.``./sd+--:/::::os-/sho---:----/+oyyyyyyso/:-.-:::+++:-:/s+:-///--+ys:....-------:/s
# MMNd+::---------...``.:hs+-:://-:::sss/--:y+++.:::--::::--:::++++s+oy:---::/+/::/ss+.`...--------:/s
# MMNm+:-:-------......``-+os/:-:///:://:-:/s/+s/+/:s+/s/oo-/oo+s+/s::+/--:++/:-/os:-......---------/s
# MMNm+:--------........```.:o++:-::/+//--:/+//+++/-h//y:os-:oy:so/:--:/+++/:-:++/.```.....--------:/o
# MMNm+:------...........`````-:+:---://++//:::-://:::/o:/+/://-////+oo+/:---:/...`...-....---------/o
# MMNm+:-------..............````....----://+++o+++o/+o+//+++ooooo++/:----....`...........----------:+
# MMNm+:---.................`...``````..-----::::////++/++////:::::----.-.`...............----------:+
# MMNm+:---..................``..`...```......-.--:--....---::-----........................--------::/
# MMNd/:--........................................--..```...-................................--.----:/
# MMNm+:--..............................................`....................................-...---:/
# MMNm+:--............................................```....................................-...---:/
# MMNm+:--..........````.````.........................````....--..--.............................---:/
# MMNm+:--........````````````````````...............`````....-...-........`````..................--:/
# MMNmo/--......````````````````````````````````...`````````.............```````````````````.......-/o
# MMMNy+:....````..`````````````````````````````````````````...........`````````````````````......--+y
# MMMMdo:-....``````````````````````````````````````````````.........``````````````````````.......-:od
# MMMMNy/-.....````````````````````````````````````````````....``...````````````````````````..``..-+yN
# MMMMMds--....``````````````````````````````````````` ````...```````````````````````````````.`..-/hmM
# MMMMMNmo:-...````````````` ``    ` ``````````````````````.````````````````````  ``````````..`.-/dNMM
# MMMMMMNdo/-...```````````      ````````````````````````...```````````````` ``````````````````:ohNMMM
# MMMMMMMNms/-....`````````````````````      ```````````.-:.`..``` ````````````````````````.../sdMMMMM
# MMMMMMMMMmh+-..`````````````   `````          `````````.-.```   `        ````          ``-:odNNMMMMM
# MMMMMMMMMMMmhs/-.````                            `     ```   `                     ``.:/ohmNMMMMMMMM
# MMMMMMMMMMMMMNmdhs+:-.`                                                       ``.-/+yhdNNNMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMNNmdyso+:--.````                                 ``..-:/+oshdmNNMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMNNmmdddhysoo+///:----........----:::///++osyhdddmNNNMMMMMMMMMMMMMMMMMMMMMMM
