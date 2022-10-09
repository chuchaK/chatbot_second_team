<script lang="ts">
  import { onMount } from "svelte";

  // store subscriptions
  type Message = {
    author: "bot" | "user";
    data: string;
  };
  type Buttons = {
    [key: number]: string[];
  };

  let messages: Message[] = [];
  let userMessage: string;
  let buttons: Buttons = {
    1: ["Блок 1, вопрос 1", "Блок 1, вопрос 2", "Блок 1, вопрос 3"],
    2: ["Блок 2, вопрос 1", "Блок 2, вопрос 2"],
    3: [
      "Блок 3, вопрос 1",
      "Блок 3, вопрос 2",
      "Блок 3, вопрос 3",
      "Блок 3, вопрос 4",
    ],
    4: [],
  
  };
  let counter: number = 1;

  let socket: WebSocket;

  onMount(() => {
    socket = new WebSocket("ws://localhost:9191/chat");
    socket.onmessage = (message) => {
      messages = [
        ...messages,
        {
          author: "bot",
          data: message.data,
        },
      ];
    };
    socket.addEventListener("open", () => {
      console.log("Opened");
    });
  });

  const sendHandler = async () => {
    socket.send(userMessage);
    messages = [
      ...messages,
      {
        author: "user",
        data: userMessage,
      },
    ];
    userMessage = "";
  };

  const questionHandler = (value: string) => {
    socket.send(value);
    messages = [
      ...messages,
      {
        author: "user",
        data: value,
      },
    ];
     counter += 1;
  };

  // $: console.log("counter", counter);
</script>
<!-- <div>
  <img class = "img_a" alt="intelligent assistent" src="Avatar.png">
  <p>Привет! Я ???.<br>
    Виртуальный помощник.</p>
  </div> -->
<div id="bodybox">
  <div id="chatborder">
    {#each messages as message}
      <p style="text-align: {message.author === 'user' ? 'right' : 'left'}">
        {message.data}
      </p>
    {/each}
    <input
      class="message"
      type="text"
      name="chat"
      bind:value={userMessage}
      placeholder="Сообщение"
    /> 
     <button type="button" class="send"on:click={sendHandler}>Send</button> 
    <p>{#each buttons[counter] as buttonText}
      <button type="button" style = "background-color: #C6B0F1;
      border-radius: 10px;
        font-family: 'Roboto', sans-serif
        font-size: 100%; height: 60%" on:click={() => questionHandler(buttonText)}
        >{buttonText}</button
      >
    {/each}</p>
  </div>
</div>
