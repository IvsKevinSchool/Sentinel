"""
Service Container Module

This module implements a Service Container (Dependency Injection Container) pattern
that allows registering and resolving service implementations by their interface contracts.

The Container class uses class methods to maintain a centralized registry of services
at the class level, meaning all registrations are shared across the application.

Key Concepts:
    - Uses @classmethod decorator to operate on the class itself, not instances
    - cls parameter refers to the class (Container), not an instance
    - _services is a class-level private attribute (single underscore convention)
    - All services are stored in a dictionary mapping interfaces to implementations

Example:
    >>> from abc import ABC, abstractmethod
    >>> 
    >>> class IUserRepository(ABC):
    ...     @abstractmethod
    ...     def get_user(self, user_id): pass
    >>> 
    >>> class UserRepository(IUserRepository):
    ...     def get_user(self, user_id):
    ...         return f"User {user_id}"
    >>> 
    >>> Container.register(IUserRepository, UserRepository())
    >>> service = Container.resolver(IUserRepository)
    >>> print(service.get_user(1))
    User 1

Notes:
    - The single underscore prefix (_services) indicates internal/private by convention
    - Class methods receive cls (the class) automatically, not self (instance)
    - This implementation follows the Service Locator pattern
"""


class Container:
    """
    A service container for dependency injection.

    This class provides a centralized registry for managing service dependencies
    using the Service Locator pattern. All operations are performed at the class
    level using class methods.

    Attributes:
        _services (dict): Class-level dictionary storing interface-implementation mappings.
                         Private by convention (single underscore prefix).

    Class Methods:
        register: Registers a service implementation for a given interface.
        resolver: Retrieves the registered implementation for a given interface.
    """
    
    _services = {}

    @classmethod
    def register(cls, interface, implementation):
        """
        Register a service implementation for a given interface.

        Args:
            interface: The interface or abstract class that defines the contract.
            implementation: The concrete implementation of the interface.

        Returns:
            None

        Example:
            >>> Container.register(IUserService, UserService())
        """
        cls._services[interface] = implementation

    @classmethod
    def resolver(cls, interface):
        """
        Resolve and return the registered implementation for a given interface.

        Args:
            interface: The interface or abstract class to resolve.

        Returns:
            The registered implementation instance.

        Raises:
            KeyError: If the interface has not been registered.

        Example:
            >>> service = Container.resolver(IUserService)
            >>> service.do_something()
        """
        return cls._services[interface]