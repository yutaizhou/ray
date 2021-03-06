from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ray import Language
from ray._raylet import JavaFunctionDescriptor

__all__ = [
    "java_function",
    "java_actor_class",
]


def format_args(worker, args, kwargs):
    """Format args for various languages.

    Args:
        worker: The global worker instance.
        args: The arguments for cross language.
        kwargs: The keyword arguments for cross language.

    Returns:
        List of args and kwargs (if supported).
    """
    if not worker.load_code_from_local:
        raise ValueError("Cross language feature needs "
                         "--load-code-from-local to be set.")
    if kwargs:
        raise TypeError("Cross language remote functions "
                        "does not support kwargs.")
    return args


def get_function_descriptor_for_actor_method(
        language, actor_creation_function_descriptor, method_name):
    """Get function descriptor for cross language actor method call.

    Args:
        language: Target language.
        actor_creation_function_descriptor:
            The function signature for actor creation.
        method_name: The name of actor method.

    Returns:
        Function descriptor for cross language actor method call.
    """
    if language == Language.JAVA:
        return JavaFunctionDescriptor(
            actor_creation_function_descriptor.class_name,
            method_name,
            # Currently not support call actor method with signature.
            "")
    else:
        raise NotImplementedError("Cross language remote actor method "
                                  f"not support language {language}")


def java_function(class_name, function_name):
    """Define a Java function.

    Args:
        class_name (str): Java class name.
        function_name (str): Java function name.
    """
    from ray.remote_function import RemoteFunction
    return RemoteFunction(
        Language.JAVA,
        lambda *args, **kwargs: None,
        JavaFunctionDescriptor(class_name, function_name, ""),
        None,  # num_cpus,
        None,  # num_gpus,
        None,  # memory,
        None,  # object_store_memory,
        None,  # resources,
        None,  # accelerator_type,
        None,  # num_returns,
        None,  # max_calls,
        None,  # max_retries
        placement_group=None,
        # TODO(ekl) set default to -1 once we support -1 as "any index"
        placement_group_bundle_index=0,
        placement_group_capture_child_tasks=None)


def java_actor_class(class_name):
    """Define a Java actor class.

    Args:
        class_name (str): Java class name.
    """
    from ray.actor import ActorClass
    return ActorClass._ray_from_function_descriptor(
        Language.JAVA,
        JavaFunctionDescriptor(class_name, "<init>", ""),
        max_restarts=0,
        max_task_retries=0,
        num_cpus=None,
        num_gpus=None,
        memory=None,
        object_store_memory=None,
        resources=None,
        accelerator_type=None,
    )
