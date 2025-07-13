from typing import Any
from collections import deque
import collections.abc # Used for checking abstract base classes if needed, but not strictly for this implementation.

class SequentialIdGenerator:
    """A class to generate sequential integer IDs, similar to an auto-incrementing sequence.

    This class provides methods to get the next ID in a sequence,
    retrieve the current ID, and reset the sequence. It's useful for
    generating unique identifiers in a controlled, predictable manner.
    """

    def __init__(self, start: int = 0):
        """Initializes the SequentialIdGenerator.

        The sequence starts from the provided `start` value. The first ID
        returned by `next()` will be `start + 1`.

        Args:
            start (int): The initial value for the sequence. Defaults to 0.
        """
        # We use a private attribute `_current_id` to store the current ID.
        # This makes it clear that it's an internal detail of the class.
        self._current_id = start

    def next_id(self) -> int:
        """Increments the sequence and returns the next ID.

        Returns:
            int: The next sequential ID.

        Example of use:
            >>> generator = SequentialIdGenerator(start=5)
            >>> generator.next_id()
            6
            >>> generator.next_id()
            7
        """
        self._current_id += 1
        return self._current_id

    def reset(self, value: int = 0) -> None:
        """Resets the sequence to a specified value.

        Args:
            value (int): The value to which the sequence should be reset. Defaults to 0.

        Example of use:
            >>> generator = SequentialIdGenerator(start=10)
            >>> generator.next_id() # Returns 11
            11
            >>> generator.reset()
            >>> generator.next_id() # Returns 1
            1
            >>> generator.reset(value=100)
            >>> generator.next_id() # Returns 101
            101
        """
        # Reset the internal counter to the specified value.
        self._current_id = value

    def get_current_id(self) -> int:
        """Returns the current ID in the sequence without incrementing.

        Returns:
            int: The current ID.

        Example of use:
            >>> generator = SequentialIdGenerator(start=10)
            >>> generator.get_current_id()
            10
            >>> generator.next_id()
            11
            >>> generator.get_current_id()
            11
        """
        return self._current_id
    

class ValueHolder:
    """A simple class to encapsulate and manage a single mutable value.

    This class acts as a container for any Python object, allowing you to
    store, retrieve, and update that value through explicit methods. It's
    useful when you need to pass a value by reference or ensure a single
    point of control for a dynamic piece of data.
    """

    def __init__(self, initial_value: Any = None):
        """Initializes the ValueHolder with an optional initial value.

        Args:
            initial_value (Any): The starting value to be held. Defaults to None.
        """
        # We use a private attribute `_stored_value` to clearly indicate
        # that it's an internal detail of the class.
        self._stored_value = initial_value

    def set_value(self, new_value: Any) -> None:
        """Sets a new value for the ValueHolder.

        Args:
            new_value (Any): The new value to store.

        Example of use:
            >>> holder = ValueHolder(10)
            >>> holder.set_value(25)
            >>> holder.get_value()
            25
        """
        self._stored_value = new_value

    def get_value(self) -> Any:
        """Retrieves the current value held by the ValueHolder.

        Returns:
            Any: The current value.

        Example of use:
            >>> holder = ValueHolder("hello")
            >>> holder.get_value()
            'hello'
            >>> holder.set_value(True)
            >>> holder.get_value()
            True
        """
        return self._stored_value   


from collections import deque


class Stack:
    """
    A versatile Stack class that can be configured to use either
    LIFO (Last-In, First-Out) or FIFO (First-In, First-Out) behavior
    internally. It also includes an option to manage duplicate elements.

    By default, it operates as a standard LIFO stack that allows duplicates.
    You can configure it to be FIFO or to disallow duplicates during
    initialization.
    """

    def __init__(self, lifo: bool = True, allow_duplicates: bool = True):
        """
        Initializes the Stack.

        Args:
            lifo (bool): If True (default), the stack behaves as LIFO.
                         If False, it behaves as FIFO.
            allow_duplicates (bool): If True (default), duplicate items can
                                     be added. If False, only unique items
                                     will be added.
        """
        self.lifo = lifo
        self.allow_duplicates = allow_duplicates
        # Using deque for O(1) appends and pops from either end,
        # which is efficient for both LIFO and FIFO.
        self.elements = deque()
        # If duplicates are not allowed, a set helps to check for existence in O(1) average time.
        # This set is essential for the 'exists' method when duplicates are not allowed.
        self.unique_elements = set() if not allow_duplicates else None

    def push(self, item) -> bool:
        """
        Adds an item to the collection.

        For LIFO mode, this adds to the "top" of the stack.
        For FIFO mode, this adds to the "back" of the queue.

        If `allow_duplicates` is False, the item will only be added if it's not
        already present in the collection.

        Args:
            item: The item to be added.

        Returns:
            bool: True if the item was successfully added, False otherwise.

        Example usage:
            # LIFO with duplicates allowed
            stack_lifo_dup = Stack(lifo=True, allow_duplicates=True)
            print(stack_lifo_dup.push(10)) # Output: True
            print(stack_lifo_dup.push(10)) # Output: True (Allowed)

            # FIFO with no duplicates
            stack_fifo_unique = Stack(lifo=False, allow_duplicates=False)
            print(stack_fifo_unique.push(20)) # Output: True
            print(stack_fifo_unique.push(20)) # Output: False (Not allowed)
            # Cost: O(1) on average for append and set operations.
        """
        if not self.allow_duplicates:
            if item in self.unique_elements:
                # Item already exists and duplicates are not allowed.
                return False
            self.unique_elements.add(item)

        self.elements.append(item)
        return True

    def pop(self):
        """
        Removes and returns an item from the collection.

        For LIFO mode, this removes from the "top" of the stack (last in).
        For FIFO mode, this removes from the "front" of the queue (first in).

        Raises:
            IndexError: If the collection is empty.

        Returns:
            The removed item.

        Example usage:
            stack_lifo = Stack(lifo=True)
            stack_lifo.push(10)
            item = stack_lifo.pop() # item will be 10 (LIFO)

            stack_fifo = Stack(lifo=False)
            stack_fifo.push(20)
            stack_fifo.push(30)
            item_fifo = stack_fifo.pop() # item_fifo will be 20 (FIFO)
            # Cost: O(1) for deque's pop and popleft, and set removal.
        """
        if not self.is_empty():
            if self.lifo:
                removed_item = self.elements.pop()
            else:
                removed_item = self.elements.popleft()

            # If duplicates are not allowed, remove the item from the unique_elements set.
            if not self.allow_duplicates:
                self.unique_elements.discard(removed_item)  # Use discard to avoid KeyError if item was already removed

            return removed_item
        else:
            raise IndexError("Cannot pop from an empty Stack.")

    def peek(self):
        """
        Returns the next item to be removed without actually removing it.

        For LIFO mode, this is the item at the "top" of the stack.
        For FIFO mode, this is the item at the "front" of the queue.

        Raises:
            IndexError: If the collection is empty.

        Returns:
            The item that would be removed next.

        Example usage:
            stack = Stack()
            stack.push(10)
            next_item = stack.peek() # next_item will be 10
            # Cost: O(1)
        """
        if not self.is_empty():
            if self.lifo:
                return self.elements[-1]
            else:
                return self.elements[0]
        else:
            raise IndexError("Cannot peek into an empty Stack.")

    def exists(self, item) -> bool:
        """
        Checks if a given item exists in the collection.

        Args:
            item: The item to check for existence.

        Returns:
            bool: True if the item is found, False otherwise.

        Example usage:
            stack = Stack(lifo=False, allow_duplicates=False)
            stack.push(10)
            print(stack.exists(10)) # Output: True
            print(stack.exists(5))  # Output: False
            # Cost: O(1) on average if allow_duplicates is False (using set lookup).
            # Cost: O(n) in worst case if allow_duplicates is True (linear search in deque).
        """
        if not self.allow_duplicates:
            # If duplicates are not allowed, we have a unique_elements set
            # for O(1) average time lookup.
            return item in self.unique_elements
        else:
            # If duplicates are allowed, we have to iterate through the deque
            # because we can't assume uniqueness. This results in O(n) worst-case.
            return item in self.elements

    def is_empty(self):
        """
        Checks if the collection is empty.

        Returns:
            bool: True if the collection is empty, False otherwise.

        Example usage:
            stack = Stack()
            is_empty_status = stack.is_empty() # is_empty_status will be True
            # Cost: O(1)
        """
        return len(self.elements) == 0

    def size(self):
        """
        Returns the number of items currently in the collection.

        Returns:
            int: The number of items.

        Example usage:
            stack = Stack()
            stack.push(1)
            collection_size = stack.size() # collection_size will be 1
            # Cost: O(1)
        """
        return len(self.elements)
    
