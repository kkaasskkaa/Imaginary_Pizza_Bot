#!/usr/bin/python3.8
from transitions import Machine
import random

class Order(object) :

    # состояния
    states = ['idle', 'orderCreated', 'pizzaSizeSelected', 'paymentMethodSelected', 'dataMistake', 'done']

    def __init__(self) :

        self.orderId = '' # номер заказа

        self.pizzaSize = '' # размер заказываемой пиццы

        self.paymentMethod = '' # способ оплаты

        # инициализация стейт-машины
        self.machine = Machine(model = self, states = Order.states, initial='idle') 

        # создание нового заказа
        self.machine.add_transition('create_order', 'idle', 'orderCreated', after = 'setOrderId')

        # выбор размера сделан
        self.machine.add_transition('select_size', 'orderCreated', 'pizzaSizeSelected')

        # выбор способа оплаты сделан
        self.machine.add_transition('select_payment_method', 'pizzaSizeSelected', 'paymentMethodSelected')

        # получение подтверждения заказа от пользователя
        self.machine.add_transition('confirm_order', 'paymentMethodSelected', 'done')

        # в заказе допущена ошибка
        self.machine.add_transition('order_mistake', 'paymentMethodSelected', 'dataMistake')

        # пользователь смирился с ошибкой и решил продолжить
        self.machine.add_transition('order_mistake_is_fine', 'dataMistake', 'paymentMethodSelected')

        # всегда можно отменить заказ
        self.machine.add_transition('reset_order', '*', 'idle', after  = 'reset')

    # обнуление заказа
    def reset_order(self) :

        self.orderId = ''   
        self.pizzaSize = '' 
        self.payMethod = '' 
        self.state = 'idle'

    # создание нового заказа
    def setOrderId(self) :

        self.orderId = random.randint(0,999999) 
        
    # установка размера пиццы
    def select_size(self, size) : 

        self.pizzaSize = size 
        self.state = 'pizzaSizeSelected'
    # установка способа оплаты
    def select_payment_method(self, method) : 

        self.paymentMethod = method 
        self.state = 'paymentMethodSelected'