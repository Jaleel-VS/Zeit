<script lang="ts">
    import type { PageData } from './$types';
    
    export let data: PageData;

    const { courseDetails } = data;


    

</script>

<div>
    <h1 class="text-4xl font-bold text-yellow-200 pb-2">Settings</h1>
    <!-- <p>Course ID: {(await courseDetails).courseID}</p>
    <p>Course Name: {(await courseDetails).courseName}</p> -->
   {#await courseDetails}
    <p>Getting results...</p>
    {:then courseDetails}
        {#if courseDetails}
            
            
            
        {:else}
            <p>No course details found</p>
        {/if}
    {:catch error}
    <p>Something went wrong: {error.message}</p>
    {/await}
</div>