<script lang="ts">
  import { Label, Input, Helper } from "flowbite-svelte";
  import { createEventDispatcher } from "svelte";
  import { isValidUrl } from "../util/course-details";
  import { debounce } from "lodash-es";

  const dispatch = createEventDispatcher();
  let url: string = "";
  let isValid: boolean = false;
  let inputColor: 'base' | 'red' | 'green' = 'base';

  const validateUrl = debounce(() => {
    isValid = isValidUrl(url);
    console.log("URL is valid:", isValid);
    inputColor = isValid ? "green" : (url.length > 0 ? "red" : "base");
  }, 300); // Debounce time of 300ms

  function handleClick() {
    dispatch("urlChange", url);
  }

  $: url, validateUrl();
</script>

<div class="flex flex-col pr-4">
  <!-- UI elements here... -->
</div>

<div class="flex flex-col pr-4">
  <Label for="url-reader" class="text-2xl font-bold text-yellow-200 pb-2"
    >Enter the course url:</Label
  >
  <Input
    id="url-reader"
    bind:value={url}
    class="w-[500px]"
    color={inputColor}

  />
  {#if inputColor == "green"}
    <Helper class="mt-2 text-xl" color="green"
      ><span class="font-small">Well done!</span> The URL is valid.</Helper
    >
  {:else if inputColor == "red"}
    <Helper class="mt-2 text-xl" color="red"
      ><span class="font-medium">Not so well done!</span> The URL is invalid.</Helper
    >
  {/if}

  <button
    class="mt-4 bg-yellow-200 hover:bg-yellow-300 text-black font-bold py-2 px-4 rounded cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
    on:click={handleClick}
    disabled={!isValid}
  >
    Search
  </button>
</div>
