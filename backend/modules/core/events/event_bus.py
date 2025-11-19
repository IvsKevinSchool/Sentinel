"""
Event Bus Module

This module implements the Observer/Publish-Subscribe pattern using an Event Bus.
It allows decoupled communication between different parts of the application through
events, where publishers emit events and subscribers react to them.

The EventBus class uses class methods to maintain a centralized registry of event
subscribers at the class level, enabling global event handling across the application.

Key Concepts:
    - Uses @classmethod decorator to operate on the class itself, not instances
    - cls parameter refers to the class (EventBus), not an instance
    - _subscribers is a class-level private attribute (single underscore convention)
    - Events are identified by string names
    - Multiple handlers can subscribe to the same event
    - Handlers are executed synchronously in subscription order

Pattern:
    This implements the Publish-Subscribe (Pub/Sub) pattern:
    - Publishers: Components that emit events using publish()
    - Subscribers: Functions/methods that react to events via suscribe()
    - Event Bus: Mediator that routes events from publishers to subscribers

Example:
    >>> # Define event handlers
    >>> def on_user_created(payload):
    ...     print(f"User created: {payload['username']}")
    >>> 
    >>> def send_welcome_email(payload):
    ...     print(f"Sending email to: {payload['email']}")
    >>> 
    >>> # Subscribe handlers to events
    >>> EventBus.suscribe('user.created', on_user_created)
    >>> EventBus.suscribe('user.created', send_welcome_email)
    >>> 
    >>> # Publish event (triggers all subscribed handlers)
    >>> EventBus.publish('user.created', {
    ...     'username': 'john_doe',
    ...     'email': 'john@example.com'
    ... })
    User created: john_doe
    Sending email to: john@example.com

Architecture Benefits:
    - Loose Coupling: Publishers don't need to know about subscribers
    - Extensibility: New handlers can be added without modifying publishers
    - Single Responsibility: Each handler focuses on one specific reaction
    - Testability: Components can be tested in isolation

Notes:
    - The single underscore prefix (_subscribers) indicates internal/private by convention
    - Class methods receive cls (the class) automatically, not self (instance)
    - Handlers are called synchronously; consider async for I/O operations
    - No error handling in handlers; exceptions will propagate to publisher
"""


class EventBus:
    """
    A centralized event bus for publish-subscribe pattern implementation.

    This class provides a global event routing mechanism where components can
    publish events and subscribe to them without direct dependencies. All
    operations are performed at the class level using class methods.

    Attributes:
        _subscribers (dict): Class-level dictionary mapping event names to lists of handlers.
                            Structure: {'event_name': [handler1, handler2, ...]}
                            Private by convention (single underscore prefix).

    Class Methods:
        suscribe: Registers a handler function to be called when an event is published.
        publish: Triggers all registered handlers for a specific event.

    Thread Safety:
        This implementation is NOT thread-safe. Consider using locks for
        concurrent access in multi-threaded environments.
    """
    
    _subscribers = {}

    @classmethod
    def suscribe(cls, event_name, handler):
        """
        Subscribe a handler function to a specific event.

        Multiple handlers can subscribe to the same event. Handlers are stored
        in a list and will be executed in the order they were subscribed when
        the event is published.

        Args:
            event_name (str): The name of the event to subscribe to.
                             Convention: Use dot notation (e.g., 'user.created', 'order.completed')
            handler (callable): A function or callable object that will be invoked when
                               the event is published. Should accept one argument (payload).

        Returns:
            None

        Example:
            >>> def log_event(payload):
            ...     print(f"Event received: {payload}")
            >>> 
            >>> EventBus.suscribe('app.started', log_event)
            >>> EventBus.suscribe('app.started', another_handler)  # Multiple handlers allowed

        Technical Details:
            Uses dict.setdefault() to create an empty list if the event_name doesn't exist,
            then appends the handler to that list. This is more concise than:
            
            if event_name not in cls._subscribers:
                cls._subscribers[event_name] = []
            cls._subscribers[event_name].append(handler)
        """
        cls._subscribers.setdefault(event_name, []).append(handler)

    @classmethod
    def publish(cls, event_name, payload):
        """
        Publish an event and trigger all subscribed handlers.

        All handlers subscribed to the event are called synchronously in the order
        they were registered. Each handler receives the payload as an argument.

        Args:
            event_name (str): The name of the event to publish.
            payload: Data to pass to all event handlers. Can be any type (dict, object, etc.)
                    Common practice is to use a dictionary for flexibility.

        Returns:
            None

        Raises:
            Any exception raised by a handler will propagate to the caller.
            Consider wrapping handler calls in try-except for production use.

        Example:
            >>> # Subscribe handlers
            >>> EventBus.suscribe('payment.processed', update_inventory)
            >>> EventBus.suscribe('payment.processed', send_receipt)
            >>> 
            >>> # Publish event with payload
            >>> EventBus.publish('payment.processed', {
            ...     'order_id': 123,
            ...     'amount': 99.99,
            ...     'customer_id': 456
            ... })

        Technical Details:
            - Uses dict.get(event_name, []) to return empty list if event has no subscribers
            - Iterates through handlers and calls each with the payload
            - Execution is synchronous and blocking
            - If no handlers are registered for the event, nothing happens (graceful)
        """
        for handler in cls._subscribers.get(event_name, []):
            handler(payload)