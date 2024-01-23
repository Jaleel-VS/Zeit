<script lang="ts">
  import { Label, Input, Helper } from "flowbite-svelte";
  import { createEventDispatcher } from "svelte";
  import { isValidUrl } from "../util/course-details";

  //   const dispatch = createEventDispatcher();

  let url: string = "";
  let esValido: boolean = false;

  let inputColor: string = "";

  // Function to validate URL
  const validateUrl = (): boolean => {
    const result = isValidUrl(url);
    console.log("URL is valid:", result);
    esValido = result;

    if (result) {
      inputColor = "green";
    } else {
      inputColor = "red";
    }

    return result;
  };

  // Reactive statement to validate URL whenever it changes
  // $: esValido = validateUrl(url);

  // Notify parent component when the button is clicked
  //   const handleSearch = () => {
  //     if (esValido) {
  //       dispatch("search", { url });
  //     } else {
  //       // Optionally handle invalid URL case
  //       console.error("Invalid URL");
  //     }
  //   };
</script>

<div class="flex flex-col pr-4">
  <Label for="url-reader" class="text-2xl font-bold text-yellow-200 pb-2"
    >Enter the course url:</Label
  >
  <Input
    id="url-reader"
    bind:value={url}
    class=""
    color={inputColor}
    placeholder="https://www.udemy.com/course/learn-flutter-dart-to-build-ios-android-apps/"
  />
  {#if inputColor == ""}{:else if inputColor == "green"}
    <Helper class="mt-2 text-xl" color="green"
      ><span class="font-small">Well done!</span> The URL is valid.</Helper
    >
  {:else if inputColor == "red"}
    <Helper class="mt-2 text-xl" color="red"
      ><span class="font-medium">Not so well done!</span> The URL is invalid.</Helper
    >
  {/if}

  <button
    class="mt-4 bg-yellow-200 hover:bg-yellow-300 text-black font-bold py-2 px-4 rounded cursor-pointer"
    on:click={validateUrl}
  >
    Search
  </button>
</div>
