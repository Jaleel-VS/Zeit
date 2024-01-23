<!-- template -->
<script>
  import img from "$lib/assets/logo.png";
</script>

<header
  class="my-2 mx-auto w-full max-w-screen-md border border-gray-100 bg-white/80 py-3 shadow backdrop-blur-lg md:top-6 md:rounded-3xl lg:max-w-screen-lg"
>
  <div class="px-4">
    <div class="flex items-center justify-between">
      <div class="flex shrink-0 items-center">
        <a
          aria-current="page"
          class="flex items-center justify-center"
          href="/"
        >
          <img class="h-20 w-auto" src={img} alt="zeit logo" />
        </a>
        <h2 class=" text-xl font-bold leading-7 text-gray-900 sm:block">
          Zeit
        </h2>
      </div>

      <div class="flex items-center justify-end gap-3">
        <a
          class="inline-flex items-center justify-center rounded-xl bg-white px-3 py-2 text-sm font-semibold text-black shadow-sm transition-all duration-150 hover:bg-slate-200 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
          href="/auth/login/">Login</a
        >
        <a
          class="items-center justify-center rounded-xl bg-black px-3 py-2 text-sm font-semibold text-white shadow-sm ring-1 ring-inset ring-gray-300 transition-all duration-150 hover:bg-slate-600 sm:inline-flex"
          href="/auth/signup/">Sign Up</a
        >
      </div>
    </div>
  </div>
</header>
