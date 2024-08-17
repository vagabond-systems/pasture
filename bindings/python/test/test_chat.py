from chat import PolygonChat

HOST = "127.0.0.1"


def print_chat(prompt, result):
    print(f"\n-------\n"
          f"( ) prompt:\n"
          f"{prompt}\n"
          f"(*) result:\n"
          f"{result}\n"
          f"-------\n")


def test_polygon_chat():
    session = PolygonChat(HOST)
    prompt = "My favorite movie is Return of the King."
    result = session.chat(prompt)
    print_chat(prompt, result)

    prompt = "Name one movie you know I like."
    result = session.chat(prompt)
    print_chat(prompt, result)


def test_polygon_tools():
    session = PolygonChat(HOST)
    prompt = "What's the weather like?"
    result = session.chat(prompt, tools=["google_search"])
    print_chat(prompt, result)


def test_polygon_pdf():
    session = PolygonChat(HOST)
    prompt = "Please provide a summary of this document."
    with open("./data/pico_sdk.pdf", "rb") as file_stream:
        file_tuples = ("pico_sdk.pdf", file_stream)
        result = session.chat(prompt, file_tuples=[file_tuples])
    print_chat(prompt, result)

    prompt = "What is this document's copyright?"
    result = session.chat(prompt)
    print_chat(prompt, result)


def test_polygon_image():
    session = PolygonChat(HOST)
    prompt = "Describe this image in flowery verse."
    with open("./data/awe.jpg", "rb") as file_stream:
        file_tuples = ("awe.jpg", file_stream)
        result = session.chat(prompt, file_tuples=[file_tuples])
    print_chat(prompt, result)


def test_chat_session_separation():
    print("first session:")
    first_session = PolygonChat(HOST)
    prompt = "I am holding two pears."
    result = first_session.chat(prompt)
    print_chat(prompt, result)

    print("second session:")
    second_session = PolygonChat(HOST)
    prompt = "I am holding twelve pears."
    result = second_session.chat(prompt)
    print_chat(prompt, result)

    print("first session rejoin:")
    first_session_rejoin = PolygonChat(HOST, port=first_session.port)
    prompt = "How many pears am I holding?"
    result = first_session_rejoin.chat(prompt)
    print_chat(prompt, result)

    print("second session rejoin:")
    second_session_rejoin = PolygonChat(HOST, port=second_session.port)
    prompt = "How many pears am I holding?"
    result = second_session_rejoin.chat(prompt)
    print_chat(prompt, result)
