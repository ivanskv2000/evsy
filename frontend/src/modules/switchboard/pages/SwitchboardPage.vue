<script setup lang="ts">
import Header from '@/shared/components/layout/PageHeader.vue'
import ResetPanel from '../components/ResetPanel.vue'
import SeedPanel from '../components/SeedPanel.vue'
import ImportPanel from '../components/ImportPanel.vue'
import ExportPanel from '../components/ExportPanel.vue'

//   import { useAppConfig } from '@/shared/composables/useAppConfig'

//   const { environment } = useAppConfig()
//   const isDevOrDemo = ['development', 'demo'].includes(environment)
</script>

<template>
  <div>
    <Header title="Switchboard" />
    <div class="container mx-auto">
      <blockquote
        class="border-border text-foreground mb-12 max-w-prose border-l-2 pl-6 text-sm leading-relaxed italic sm:text-base"
      >
        “We do not succeed in changing things in accordance with our desires, but gradually our desires change.”
        <footer class="text-muted-foreground mt-2 text-xs not-italic">— Marcel Proust, <span class="italic">In Search of Lost Time</span></footer>
      </blockquote>
      <div class="space-y-6 mb-24">
        <ResetPanel />
        <SeedPanel />
        <ExportPanel />
        <ImportPanel />
      </div>
    </div>
  </div>
</template>
