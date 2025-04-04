import asyncio
import curses

MAX_MESSAGE_SIZE = 1024  # Maximum allowed message size in bytes

# No changes here since you already understand this:
async def handle_server_messages(client_socket, chat_window):
    """Receive and display messages from the server."""
    while True:
        try:
            message = await client_socket.recv(1024)
            if not message:
                break
            chat_window.addstr(f"Server: {message.decode('utf-8')}\n")
            chat_window.refresh()
        except Exception as e:
            chat_window.addstr(f"Error: {e}\n")
            chat_window.refresh()
            break

async def chat_client(stdscr, host='localhost', port=8888):
    """Main chat client with curses interface."""
    # Setup curses interface
    curses.curs_set(1)  # Show the cursor for typing
    stdscr.clear()  # Clear the entire screen
    chat_window = stdscr.subwin(curses.LINES - 3, curses.COLS, 0, 0)  # Window for displaying chat messages
    input_window = stdscr.subwin(3, curses.COLS, curses.LINES - 3, 0)  # Window for user input
    input_window.border()  # Add a border around the input window
    input_window.addstr(1, 1, "> ")  # Display a prompt to start user input

    # Connect to the server asynchronously
    client_socket = await asyncio.open_connection(host, port)
    reader, writer = client_socket  # Split connection into reader/writer streams

    # Launch a separate coroutine to handle messages from the server
    asyncio.create_task(handle_server_messages(reader, chat_window))

    # Main input loop for the client
    user_input = ""  # Initialize the user input buffer
    while True:
        try:
            # Get user input one character at a time
            char = input_window.getch(1, len(user_input) + 3)  # Fetch the next typed character
            if char == curses.KEY_BACKSPACE or char == 127:  # Handle backspace key
                user_input = user_input[:-1]  # Remove last character from the input buffer
            elif char == 10:  # Handle enter key
                if len(user_input.encode('utf-8')) > 0:  # Check if input is non-empty
                    writer.write(user_input.encode('utf-8'))  # Send the message to the server
                    await writer.drain()  # Ensure data is sent immediately
                    chat_window.addstr(f"You: {user_input}\n")  # Display user's message in the chat window
                    chat_window.refresh()  # Refresh the chat window to show the new message
                    user_input = ""  # Clear the input buffer after sending
            elif len(user_input.encode('utf-8')) < MAX_MESSAGE_SIZE:  # Restrict input to maximum size
                user_input += chr(char)  # Append typed character to input buffer
            else:
                input_window.addstr(2, 1, "Message too long!")  # Display error message if input exceeds limit
            
            # Update input field with the current buffer
            input_window.clear()  # Clear the input window
            input_window.border()  # Redraw the border
            input_window.addstr(1, 1, f"> {user_input}")  # Display current input buffer
            input_window.refresh()  # Refresh input window to show updates
        
        except Exception as e:
            chat_window.addstr(f"Error: {e}\n")  # Log exceptions in chat window
            chat_window.refresh()  # Refresh chat window to show error message
            break  # Exit input loop on error

# Initialize curses wrapper with the asyncio client
asyncio.run(curses.wrapper(chat_client))