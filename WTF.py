
import random
import os
import json

SAVE_FILE = "progreso_juego.json"

estado = {
    "dinero": 100,
    "vidas": 3,
    "inventario": [],
    "logros": [],
    "dificultad": "normal"
}

objetos = {
    "vida extra": 50,
    "ver carta oculta del bot": 30,
    "doble apuesta": 70,
    "reducir bot 1 punto": 40
}

logros_definidos = {
    "primer victoria": "Ganaste tu primera ronda.",
    "rico": "Acumulaste $200 o más.",
    "superviviente": "Jugaste 5 rondas sin perder todas tus vidas.",
    "comprador": "Compraste tu primer objeto.",
    "estratega": "Usaste un objeto en el momento justo."
}

rondas_jugadas = 0

def guardar_estado():
    with open(SAVE_FILE, "w") as f:
        json.dump(estado, f)

def cargar_estado():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            datos = json.load(f)
            estado.update(datos)

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def mostrar_estado():
    print(f"\n💰 Dinero: ${estado['dinero']} | ❤️ Vidas: {estado['vidas']} | 🧰 Inventario: {estado['inventario']}")
    print(f"🌟 Dificultad: {estado['dificultad']} | 🏆 Logros: {len(estado['logros'])}")

def desbloquear_logro(clave):
    if clave not in estado["logros"]:
        estado["logros"].append(clave)
        print(f"\n🏆 ¡Logro desbloqueado! {logros_definidos[clave]}")

def turno_jugador():
    total = 0
    while True:
        print(f"\nTu total actual es: {total}")
        elegir = input("¿Querés sacar una carta? (s/n): ").lower()
        if elegir == "s":
            carta = random.randint(1, 6)
            print(f"🃏 Sacaste un {carta}")
            total += carta
            if total > 16:
                print("💥 ¡Te pasaste de 16!")
                return 0
        else:
            return total

def turno_bot():
    dificultad = estado["dificultad"]
    limite = {"facil": 10, "normal": 12, "dificil": 14}.get(dificultad, 12)
    total = 0
    while total < limite:
        total += random.randint(1, 6)
    return total if total <= 16 else 0

def jugar_ronda():
    global rondas_jugadas
    limpiar_pantalla()
    mostrar_estado()
    try:
        apuesta = int(input("\n¿Cuánto querés apostar?: "))
        if apuesta > estado["dinero"] or apuesta <= 0:
            print("❌ Apuesta inválida.")
            return
    except ValueError:
        print("❌ Ingresá un número válido.")
        return

    usar_obj = None
    if estado["inventario"]:
        print(f"\nObjetos disponibles: {estado['inventario']}")
        usar_obj = input("¿Querés usar alguno? (escribí el nombre exacto o enter): ").strip()
        if usar_obj not in estado["inventario"]:
            usar_obj = None
        else:
            estado["inventario"].remove(usar_obj)
            desbloquear_logro("estratega")

    jugador_score = turno_jugador()
    bot_score = turno_bot()

    if usar_obj == "ver carta oculta del bot":
        print(f"(Vista previa) 🤖 Bot sacó: {bot_score}")
    elif usar_obj == "reducir bot 1 punto":
        bot_score = max(0, bot_score - 1)

    if usar_obj == "doble apuesta":
        apuesta *= 2

    print(f"\nTu puntaje: {jugador_score}")
    print(f"Puntaje del bot: {bot_score}")

    if jugador_score > bot_score:
        print(f"🎉 ¡Ganaste ${apuesta}!")
        estado["dinero"] += apuesta
        desbloquear_logro("primer victoria")
        if estado["dinero"] >= 200:
            desbloquear_logro("rico")
    elif jugador_score < bot_score:
        print(f"😢 Perdiste ${apuesta}")
        estado["dinero"] -= apuesta
        estado["vidas"] -= 1
    else:
        print("🤝 Empate. No ganás ni perdés dinero.")

    rondas_jugadas += 1
    if rondas_jugadas >= 5:
        desbloquear_logro("superviviente")

    guardar_estado()

def tienda():
    limpiar_pantalla()
    print("🏪 Bienvenido a la tienda\n")
    for i, (objeto, precio) in enumerate(objetos.items(), 1):
        print(f"{i}. {objeto} - ${precio}")
    print(f"{len(objetos)+1}. Salir")

    try:
        opcion = int(input("\nElegí una opción: "))
        if 1 <= opcion <= len(objetos):
            objeto = list(objetos.keys())[opcion - 1]
            precio = objetos[objeto]
            if estado["dinero"] >= precio:
                if objeto == "vida extra":
                    estado["vidas"] += 1
                else:
                    estado["inventario"].append(objeto)
                estado["dinero"] -= precio
                desbloquear_logro("comprador")
                print(f"✅ Compraste {objeto}")
            else:
                print("❌ No tenés suficiente dinero.")
        else:
            print("Saliendo de la tienda...")
    except ValueError:
        print("❌ Opción inválida.")

    guardar_estado()

def elegir_dificultad():
    print("\nSeleccioná la dificultad:")
    print("1. Fácil")
    print("2. Normal")
    print("3. Difícil")
    eleccion = input("Opción: ")
    estado["dificultad"] = {
        "1": "facil",
        "2": "normal",
        "3": "dificil"
    }.get(eleccion, "normal")

def menu():
    cargar_estado()
    if not os.path.exists(SAVE_FILE):
        elegir_dificultad()
        guardar_estado()

    while estado["vidas"] > 0 and estado["dinero"] > 0:
        print("\n=== 🎮 Juego: No superar los 16 ===")
        print("1. Jugar una ronda")
        print("2. Ir a la tienda")
        print("3. Ver logros")
        print("4. Salir")
        opcion = input("Elegí una opción: ")
        if opcion == "1":
            jugar_ronda()
        elif opcion == "2":
            tienda()
        elif opcion == "3":
            print("\n🏆 Logros desbloqueados:")
            for l in estado["logros"]:
                print(f"- {logros_definidos[l]}")
        elif opcion == "4":
            print("👋 ¡Gracias por jugar!")
            break
        else:
            print("❌ Opción inválida.")

    if estado["vidas"] <= 0:
        print("💀 Te quedaste sin vidas. Fin del juego.")
    elif estado["dinero"] <= 0:
        print("💸 Te quedaste sin dinero. Fin del juego.")
    guardar_estado()

if __name__ == "__main__":
    menu()
