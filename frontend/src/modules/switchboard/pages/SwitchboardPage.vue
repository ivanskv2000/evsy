<script setup lang="ts">
import Header from '@/shared/components/layout/PageHeader.vue'
import ResetPanel from '../components/ResetPanel.vue'
import SeedPanel from '../components/SeedPanel.vue'
import ImportPanel from '../components/ImportPanel.vue'
import ExportPanel from '../components/ExportPanel.vue'
import { useAppConfig } from '@/shared/composables/useAppConfig'

const { isProd, isDev } = useAppConfig()
</script>

<template>
  <div>
    <Header title="Switchboard" />
    <div class="container mx-auto">
      <figure
        class="border-border text-foreground mb-12 max-w-prose border-l-2 pl-6 text-sm leading-relaxed italic sm:text-base"
      >
        <blockquote>
          “We do not succeed in changing things in accordance with our desires, but gradually our
          desires change.”
        </blockquote>
        <footer class="text-muted-foreground mt-3 text-xs not-italic">
          — Marcel Proust, <span class="italic">In Search of Lost Time</span>
        </footer>
      </figure>

      <div class="mb-24 space-y-12">
        <ResetPanel v-if="isDev || isProd" />
        <SeedPanel v-if="isDev" />
        <ExportPanel />
        <ImportPanel v-if="isDev || isProd" />
      </div>
    </div>
  </div>
</template>
