<script>
    import "../app.pcss";
    import Navbar from "$lib/components/Navbar.svelte";
  </script>
  
  <div class="main">
      <Navbar />
      <div class="content mx-auto pt-2">
          <slot />
      </div>
  </div>
  
  <style lang="postcss">
      .main {
          display: grid;
          grid-template-rows: auto 1fr; /* Define two rows: one for the Navbar and one for the content */
          height: 100vh; /* Adjust the height as needed */
      }
  
      .content {
          
      }
  </style>
  