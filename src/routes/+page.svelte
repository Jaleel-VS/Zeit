<script lang="ts">
  import URLInput from "$lib/components/URLInput.svelte";
  import { getCourseDetails } from "$lib/util/course-details";
  let udemyUrl: string = "";
  let courseID: string | null= "";
  let courseName: string | null = "";

  const handleSearch = (event: any) => {
    console.log("Event from child:", event);
    console.log("URL from child:", event.detail);
    udemyUrl = event.detail;
    // Add your logic to handle the URL here
  };

  const obtenDetallesDelCurso = async() => {
    console.log("Obteniendo detalles del curso...");
    const courseDetails = await getCourseDetails(udemyUrl);
    courseID = courseDetails['courseId'];
    courseName = courseDetails['courseTitle'];
  };

  const handleClick = () => {
    console.log("I've been clicked in the parent!");
  };
</script>

<div class="container">
  <URLInput on:urlChange={handleSearch}></URLInput>
  {#if udemyUrl}
   <button on:click={
    () => obtenDetallesDelCurso()
   }
   class="mt-4 bg-yellow-200 hover:bg-yellow-300 text-black font-bold py-2 px-4 rounded cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
   >Obtener detalles del curso</button>
   {#if courseID}
    <p>URL: {udemyUrl}</p>
    <p>Course ID: {courseID}</p>
    <p>Course Name: {courseName}</p>
    {:else}
    <p>Getting results...</p>
    {/if}
  {/if}
</div>
