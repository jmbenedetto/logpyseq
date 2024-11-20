import requests
import json

# Doc site: https://plugins-doc.logseq.com/ .
# This list is auto-generated from https://github.com/logseq/plugins/tree/master/docs .
apis = [
    "logseq.settings",
    "logseq.updateSettings",
    "logseq.once",
    "logseq.toggleMainUI",
    "logseq.listeners",
    "logseq.ready",
    "logseq.connected",
    "logseq.removeListener",
    "logseq.showMainUI",
    "logseq.resolveResourceFullUrl",
    "logseq.provideStyle",
    "logseq.caller",
    "logseq.addListener",
    "logseq.hideSettingsUI",
    "logseq.provideUI",
    "logseq.setMainUIInlineStyle",
    "logseq.emit",
    "logseq.showSettingsUI",
    "logseq.listenerCount",
    "logseq.removeAllListeners",
    "logseq.onSettingsChanged",
    "logseq.provideTheme",
    "logseq.Experiments",
    "logseq.eventNames",
    "logseq.FileStorage",
    "logseq.provideModel",
    "logseq.baseInfo",
    "logseq.setMainUIAttrs",
    "logseq.useSettingsSchema",
    "logseq.hideMainUI",
    "logseq.isMainUIVisible",
    "logseq.beforeunload",
    "logseq.UI.showMsg",
    "logseq.UI.closeMsg",
    "logseq.App.registerPageMenuItem",
    "logseq.App.getUserInfo",
    "logseq.App.setRightSidebarVisible",
    "logseq.App.showMsg",
    "logseq.App.quit",
    "logseq.App.registerUIItem",
    "logseq.App.setFullScreen",
    "logseq.App.onMacroRendererSlotted",
    "logseq.App.getInfo",
    "logseq.App.onPageHeadActionsSlotted",
    "logseq.App.onCurrentGraphChanged",
    "logseq.App.registerCommandShortcut",
    "logseq.App.getStateFromStore",
    "logseq.App.onSidebarVisibleChanged",
    "logseq.App.registerCommand",
    "logseq.App.setLeftSidebarVisible",
    "logseq.App.replaceState",
    "logseq.App.setZoomFactor",
    "logseq.App.execGitCommand",
    "logseq.App.invokeExternalCommand",
    "logseq.App.queryElementById",
    "logseq.App.onThemeModeChanged",
    "logseq.App.openExternalLink",
    "logseq.App.pushState",
    "logseq.App.getCurrentGraph",
    "logseq.App.onRouteChanged",
    "logseq.App.queryElementRect",
    "logseq.App.registerCommandPalette",
    "logseq.App.relaunch",
    "logseq.App.getUserConfigs",
    "logseq.App.onBlockRendererSlotted",
    "logseq.DB.datascriptQuery",
    "logseq.DB.onChanged",
    "logseq.DB.q",
    "logseq.DB.onBlockChanged",
    "logseq.Assets.listFilesOfCurrentGraph",
    "logseq.Editor.insertBatchBlock",
    "logseq.Editor.getAllPages",
    "logseq.Editor.createPage",
    "logseq.Editor.getBlockProperty",
    "logseq.Editor.getBlockProperties",
    "logseq.Editor.insertAtEditingCursor",
    "logseq.Editor.getCurrentPage",
    "logseq.Editor.appendBlockInPage",
    "logseq.Editor.getSelectedBlocks",
    "logseq.Editor.insertBlock",
    "logseq.Editor.getPagesTreeFromNamespace",
    "logseq.Editor.onInputSelectionEnd",
    "logseq.Editor.scrollToBlockInPage",
    "logseq.Editor.moveBlock",
    "logseq.Editor.getPreviousSiblingBlock",
    "logseq.Editor.exitEditingMode",
    "logseq.Editor.getPagesFromNamespace",
    "logseq.Editor.getNextSiblingBlock",
    "logseq.Editor.getPage",
    "logseq.Editor.renamePage",
    "logseq.Editor.prependBlockInPage",
    "logseq.Editor.deletePage",
    "logseq.Editor.editBlock",
    "logseq.Editor.checkEditing",
    "logseq.Editor.getCurrentPageBlocksTree",
    "logseq.Editor.getCurrentBlock",
    "logseq.Editor.upsertBlockProperty",
    "logseq.Editor.registerSlashCommand",
    "logseq.Editor.getPageBlocksTree",
    "logseq.Editor.getPageLinkedReferences",
    "logseq.Editor.updateBlock",
    "logseq.Editor.registerBlockContextMenuItem",
    "logseq.Editor.removeBlock",
    "logseq.Editor.restoreEditingCursor",
    "logseq.Editor.removeBlockProperty",
    "logseq.Editor.getBlock",
    "logseq.Editor.openInRightSidebar",
    "logseq.Editor.setBlockCollapsed",
    "logseq.Editor.getEditingBlockContent",
    "logseq.Editor.getEditingCursorPosition",
    "logseq.Git.saveIgnoreFile",
    "logseq.Git.loadIgnoreFile",
    "logseq.Git.execCommand",
]


def raw_api_call(host, port, token, method, args):
    """
    Makes a raw API call to the specified host and port using the provided token, method, and arguments.

    Args:
        host (str): The hostname or IP address of the API server.
        port (int): The port number on which the API server is listening.
        token (str): The authorization token to be included in the request headers.
        method (str): The API method to be called.
        args (dict): The arguments to be passed to the API method.

    Returns:
        dict or str: The JSON response from the API if the response can be decoded as JSON, otherwise the raw text response.
    """
    resp = requests.post(
        f"http://{host}:{port}/api",
        json={"method": method, "args": args},
        headers={"Authorization": "Bearer " + token},
    )
    try:
        return resp.json()
    except json.JSONDecodeError:
        return resp.text


def _define_api(host, port, token, cls, method):
    """
    Defines an API method on a given class.

    This function dynamically creates a method on the specified class (`cls`)
    based on the provided `method` string. The method will be a static method
    that wraps a call to `raw_api_call` with the given `host`, `port`, `token`,
    and method arguments.

    Args:
        host (str): The host address for the API.
        port (int): The port number for the API.
        token (str): The authentication token for the API.
        cls (type): The class on which the method will be defined.
        method (str): The fully qualified name of the method to be defined,
                      with namespaces separated by dots.

    Example:
        If `method` is "namespace.subnamespace.methodName", this function will
        create the necessary nested namespaces on `cls` and define `methodName`
        as a static method within the innermost namespace.

    Returns:
        None
    """
    [_, *hier, name] = method.split(".")

    @staticmethod
    def _wrap(*args):
        return raw_api_call(host, port, token, method, args)

    if hier:
        for ns in hier:
            if not hasattr(cls, ns):
                setattr(cls, ns, type(ns, (object,), {}))
            cls = getattr(cls, ns)
    setattr(cls, name, _wrap)


def _create_class(host, port, token):
    """
    Dynamically creates a Logseq class with methods defined by the provided APIs.

    Args:
        host (str): The host address for the API.
        port (int): The port number for the API.
        token (str): The authentication token for the API.

    Returns:
        type: A dynamically created Logseq class with methods defined by the provided APIs.
    """

    class Logseq:
        pass

    for api in apis:
        _define_api(host, port, token, Logseq, api)
    return Logseq


def logseq(token, host="127.0.0.1", port="12315"):
    """
    Creates and returns an instance of a class for logging sequences.

    Args:
        token (str): The authentication token required for LogSeq graph connection.
        host (str, optional): The host address of LogSeq graph. Defaults to "127.0.0.1".
        port (str, optional): The port number of the LogSeq graph. Defaults to "12315".

    Returns:
        object: An instance of the LogSeq class.
    """
    return _create_class(host, port, token)()


# Exemple Usage:
# mygraph = logseq("127.0.0.1", "12315", logseq_token)
# mygraph.Editor.createPage("APITest")
# mygraph.Editor.checkEditing()
# mygraph.Editor.appendBlockInPage("APITest", "Block 1")
# mygraph.Editor.appendBlockInPage("APITest", "Block 2")
# mygraph.App.showMsg("Hello!")
# import time

# time.sleep(10)
# mygraph.Editor.deletePage("APITest")


def upsert_page_properties(logseq_graph, page_uuid: str, target: dict):
    """
    - Set target_property value to target_value in page_uuid.
    - If target property does not exist it will be created.
    - With the bug in upsertBlockProperty endpoint, we must re-write
    the entire page property string using updateBlock.
    - LogSeq API converts property keys to camelCase, so we must convert
    them to snake_case before updating.

    logseq_graph: logseq connected graph object
    page_uuid: str - UUID of the page to update. Only one page can be updated at a time.
    target: dict - Dictionary with target_property(str) as keys and target_value(str) as values.
    """

    def to_snake_case(camel_str):
        return re.sub(r"(?<!^)(?=[A-Z])", "_", camel_str).lower()

    property_dict = logseq_graph.Editor.getBlock(page_uuid)["propertiesTextValues"]
    property_dict = {to_snake_case(k): v for k, v in property_dict.items()}

    for property, value in target.items():
        property_dict[property] = value
        print(f"Update page {page_uuid} with {property}={value}")

    property_str = (
        str(property_dict)[1:-1]
        .replace("'", "")
        .replace(": ", ":: ")
        .replace(", ", "\n")
        + "\n"
    )
    logseq_graph.Editor.updateBlock(page_uuid, property_str)
    print("Update completed")
    return

# Example Usage:
# from logpyseq import logseq, upsert_page_properties
# logseq_token = "your_logseq_token"
# mygraph = logseq(logseq_token, host="127.0.0.1", port="12315")
# page_uuid = "your_page_uuid"
# target_properties = {
#     "property_name1": "property_value1",
#     "property_name2": "property_value2",
#     "property_name3": "property_value3"
# }
# upsert_page_properties(mygraph, page_uuid, target_properties)
