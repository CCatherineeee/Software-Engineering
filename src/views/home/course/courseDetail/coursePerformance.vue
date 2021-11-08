<template>
  <v-card>
    <v-card-title>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="performance"
      :search="search"
    ></v-data-table>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      search: "",
      headers: [
        {
          text: "实验时间",
          align: "start",
          filterable: false,
          value: "time",
        },
        { text: "实验名称", value: "title" },
        { text: "得分", value: "score" },
      ],
      performance: [
        {
          time: 159,
          title: "Frozen Yogurt",
          score: 6.0,
        },
        {
          time: 237,
          title: "Ice cream sandwich",
          score: 9.0,
        },
        {
          time: 262,
          title: "Eclair",
          score: 16.0,
        },
        {
          time: 305,
          title: "Cupcake",
          score: 3.7,
        },
        {
          time: 356,
          title: "Gingerbread",
          score: 16.0,
        },
        {
          time: 375,
          title: "Jelly bean",
          score: 0.0,
        },
        {
          time: 392,
          title: "Lollipop",
          score: 0.2,
        },
        {
          time: 408,
          title: "Honeycomb",
          score: 3.2,
        },
        {
          time: 452,
          title: "Donut",
          score: 25.0,
        },
        {
          time: 518,
          title: "KitKat",
          score: 26.0,
        },
      ],
    };
  },
};
</script>