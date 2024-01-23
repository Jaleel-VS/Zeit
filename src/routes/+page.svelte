<script lang="ts">
  import URLInput from "$lib/components/URLInput.svelte";

  const handleSearch = (event: any) => {
    console.log("URL from child:", event.detail.url);
    // Add your logic to handle the URL here
  };

  const handleClick = () => {
    console.log("I've been clicked in the parent!");
  };
</script>

<div class="container">
  <URLInput />
</div>
