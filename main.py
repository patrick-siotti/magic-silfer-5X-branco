from requests import get
from datetime import datetime, date
from time import sleep as sl
from threading import Thread


def geral():
    while True:
        try:
            lista_atua = []
            lista = []
            dicte = {}
            melhor_lista = []
            T_F_1 = True
            final = []
            id_parcial = None
            dict_grupo_geral = {'green': 0, 'loss': 0}

            def hor():
                global T_F_1
                global  lista_atua
                lista_atua = []
                T_F_1 = False
                date_now = date.today()
                hora = datetime.today().hour
                while True:
                    try:
                        if hora == 0:
                            i = ['00:00:00', '12:00:00']
                        else:
                            i = ['12:00:00', '00:00:00']
                            date_1 = date.today().day - 1
                            date_now = date.today().replace(day=date_1)
                        r = eval(
                            get(f'https://blaze.com/api/roulette_games/history?startDate={date_now}T{i[0]}Z&endDate={date.today()}T{i[1]}Z&page=1').text)
                        pag = int(r['total_pages'])
                        print('iniciando looping')
                        for n in range(pag, 0, -1):
                            req = eval(
                                get(f'https://blaze.com/api/roulette_games/history?startDate={date_now}T{i[0]}Z&endDate={date.today()}T{i[1]}Z&page={n}').text)
                            for resultado in req['records'][::-1]:
                                lista_atua.append(int(resultado['roll']))
                    except IndexError:
                        continue
                print('LOOP DE ESTRATEGIA')
                for n1 in range(0, 15):
                    for n2 in range(0, 15):
                        for n3 in range(0, 15):
                            lista.append([n1, n2, n3])
                            dicte[(n1, n2, n3)] = {'green': 0, 'red': 0}

                for i in range(0, len(lista_atua)):
                    for i1 in lista:
                        i2 = 3
                        T_F = False
                        try:
                            if [lista_atua[i], lista_atua[i + 1], lista_atua[i + 2]] == i1:
                                v = tuple(i1)
                                for quan in range(1, 6):
                                    if lista_atua[i + i2] == 0:
                                        T_F = True
                                        dicte[v]['green'] += 1
                                        break
                                    i2 += 1

                                if not T_F:
                                    dicte[v]['red'] += 1


                        except IndexError:
                            break
                print('LOOP VERIFICAÇAO')
                for valor in dicte.keys():
                    if dicte[valor]['green'] > 0:
                        try:
                            soma_red = dicte[valor]['green'] + dicte[valor]['red']
                            por_red = dicte[valor]['green'] * 100 / soma_red
                            if por_red > 99:
                                if dicte[valor]['green'] > 0:
                                    print(valor, dicte[valor])
                                    melhor_lista.append(list(valor))

                        except ZeroDivisionError:
                            break
                T_F_1 = True

            def loop():
                print('FUNCIONANDO')
                while True:
                    try:
                        hora_min = [datetime.today().hour, datetime.today().minute]
                        print(hora_min)
                        if hora_min == [0, 1]:
                            hor()
                        if hora_min == [12, 1]:
                            hor()
                    except:
                        continue

            def sinais():
                if T_F_1:
                    print(melhor_lista)
                    global id_parcial
                    id_ent = None  # teste
                    ide = '6074391515:AAFIKPBMiEyo5KsyhcLvWMwQk98ix8F92t8'
                    id = ' -1001913134268'
                    stickers_loss = 'CAACAgEAAxkBAAEV-ZRi0CEHy0s0uYaIsv6RzqJ_4RlpewACGAIAAp0pKUW3qhl-6XSkwikE'
                    stickers_branco = 'CAACAgEAAxkBAAEV-aRi0CM01C2fXvxjej6OZ8f0NAzvbgACjgEAAmZluEUPF-6vdM99sCkE'
                    for melhor in melhor_lista:
                        if melhor == final:
                            print('branco encontrado')
                            mensagem = f'''    🤍🤍🤍🤍.........ATENÇÃO.........🤍🤍🤍🤍
                
                   🔥FAZER 5 ENTRADAS🔥
                
                
                POSSIBILIDADE DE BRANCO:🤍
                
                APÓS:{final[4:]}
                
                   📈SIGAM O GERENCIAMENTO📈'''
                            get(f'https://api.telegram.org/bot{ide}/sendMessage?chat_id={id}&text={mensagem}')
                            t = 0
                            while True:
                                try:
                                    result = get('https://blaze.com/api/roulette_games/current').json()
                                except:
                                    print("Error decoding JSON!")
                                else:
                                    if result['status'] == 'rolling':
                                        if id_ent:
                                            get(f'https://api.telegram.org/bot{ide}/deleteMessage?chat_id={id}&message_id={id_ent}')
                                        t += 1
                                        n = result['roll']
                                        mensag = f'ENTRADA DE N°:{t}\n SAIU:{n}'
                                        r = get(
                                            f'https://api.telegram.org/bot{ide}/sendMessage?chat_id={id}&text={mensag}').json()
                                        id_ent = r['result']['message_id']
                                        if result['roll'] == 0:
                                            get(f'https://api.telegram.org/bot{ide}/sendSticker?chat_id={id}&sticker={stickers_branco}')
                                            dict_grupo_geral['green'] += 1
                                            sl(14)
                                            break
                                        if t > 4:
                                            get(f'https://api.telegram.org/bot{ide}/sendSticker?chat_id={id}&sticker={stickers_loss}')
                                            dict_grupo_geral['loss'] += 1
                                            break
                                        sl(10)

                            try:
                                soma = dict_grupo_geral['green'] + dict_grupo_geral['loss']
                                por = dict_grupo_geral['green'] * 100 / soma
                                green = dict_grupo_geral['green']
                                loss = dict_grupo_geral['loss']
                                mensage = f'PARCIAL ✅={green} ⛔={loss} \n   🎯: {por:.2f} de acerto '
                                if id_parcial:
                                    get(f'https://api.telegram.org/bot{ide}/deleteMessage?chat_id={id}&message_id={id_parcial}')
                                r = get(
                                    f'https://api.telegram.org/bot{ide}/sendMessage?chat_id={id}&text={mensage}').json()
                                id_parcial = r['result']['message_id']
                            except ZeroDivisionError:
                                pass

            def verificarstatus():
                print('FUNCIONANDO')
                while True:
                    sl(16)
                    while True:
                        try:
                            result = get('https://blaze.com/api/roulette_games/current').json()
                            output = get('https://blaze.com/api/roulette_games/recent').json()
                        except:
                            print("Error decoding JSON!")
                            continue
                        else:
                            if result['status'] == 'complete':
                                sl(1)
                                global final
                                final1 = [row['roll'] for row in output[:3]]
                                final = [final1[2], final1[1], final1[0]]

                                break

                    sl(1)
                    print('saindo')
                    sinais()

            Thread(target=loop).start()
            Thread(target=verificarstatus).start()
        except:
            continue


geral()
