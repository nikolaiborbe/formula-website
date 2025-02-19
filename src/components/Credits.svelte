<script>
  import HoverInfo from "./HoverInfo.svelte";
</script>

<div class="w-full h-14 flex items-center justify-around">
  <!-- GitHub Icon with Tooltip -->
  <HoverInfo text="GitHub">
    <a href="https://github.com/nikolaiborbe" target="_blank" rel="noopener noreferrer">
      <svg role="img" viewBox="0 0 24 24" fill="currentColor" width="32" height="32" xmlns="http://www.w3.org/2000/svg">
        <title>GitHub</title>
        <path d="M12 0C5.37 0 0 5.373 0 12c0 5.303 3.438 9.8 8.205 11.387.6.113.82-.258.82-.577v-2.234c-3.338.724-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.84 1.236 1.84 1.236 1.07 1.833 2.807 1.304 3.492.997.108-.775.42-1.304.762-1.604-2.665-.3-5.467-1.332-5.467-5.93 0-1.31.468-2.38 1.235-3.22-.123-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.29-1.552 3.295-1.23 3.295-1.23.655 1.653.243 2.874.12 3.176.77.84 1.232 1.91 1.232 3.22 0 4.61-2.807 5.625-5.48 5.92.432.372.816 1.102.816 2.222v3.293c0 .319.218.694.825.576C20.565 21.796 24 17.303 24 12c0-6.627-5.373-12-12-12"/>
      </svg>
    </a>
  </HoverInfo>

  <!-- Buy Me A Coffee Icon with HoverInfo -->
  <HoverInfo text="Support my work">
    <a href="https://buymeacoffee.com/nikolaiborbe" target="_blank" rel="noopener noreferrer">
      <img src="buymeacoffee.png" alt="Buy Me A Coffee" style="height:32px;">
    </a>
  </HoverInfo>

  <!-- Profile Icon (Circular) with HoverInfo -->
  <HoverInfo text="Me">
    <a href="https://nikolai.vip/" target="_blank" rel="noopener noreferrer">
      <div class="rounded-full overflow-hidden" style="width:32px; height:32px;">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
          <title>Profile</title>
          <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8V22h19.2v-2.8c0-3.2-6.4-4.8-9.6-4.8z"/>
        </svg>
      </div>
    </a>
  </HoverInfo>
</div>
