class Jar:
    def __init__(self, capacity =12):
        if capacity < 0 :
            raise ValueError("Wrong Capacity")
        self._capacity = capacity
        self._size = 0

    def __str__(self):
        return self._size * '🍪'

    def deposit(self, n):
        if n > self.capacity:
            raise ValueError("Jar is Full!")
        if self._size + n <= self.capacity:
            self._size += n
        else:
            raise ValueError("Jar is Full!")

    def withdraw(self, n):
        if self._size < n:
             raise ValueError("Not enough Cookies!")
        else:
            self._size -= n


    @property
    def capacity(self):
        return self._capacity

    @property
    def size(self):
       return(self._size)

def main():
    jar = Jar()
    print(jar.capacity)
    jar.deposit(5)
    print(jar)
    print(jar.size)
    jar.withdraw(3)
    print(jar)

main()

