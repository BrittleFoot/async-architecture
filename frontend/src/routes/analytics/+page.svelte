<script lang="ts">
	import { AnalyticsService, type Day } from '$lib/api/analytics.js';
	import DaysAnalyticsWidget from '$lib/components/DaysAnalyticsWidget.svelte';
	import Skeleton from '$lib/components/Skeleton.svelte';
	import { onMount } from 'svelte';

	export let data;


    const analytics = new AnalyticsService(data.tokenInfo.accessToken);

    let dayPromise = Promise.resolve<Day[]>([]);

    onMount(() => {
        dayPromise = analytics.getDayAnalytics();
    });

</script>

<h1>Analytics</h1>


{#await dayPromise}
    <Skeleton width="100%" height="16em" primaryColor="#1a202ccc" secondaryColor="#FFFFFF33"/>
{:then days}
    <DaysAnalyticsWidget {days}/>
{:catch error}
    <p>{error.message}</p>
{/await}
