interface ISiteMetadataResult {
  siteTitle: string;
  siteUrl: string;
  description: string;
  keywords: string;
  logo: string;
  navLinks: {
    name: string;
    url: string;
  }[];
}

const data: ISiteMetadataResult = {
  siteTitle: 'Workouts Map',
  siteUrl: 'https://github.com/flyfish321',
  logo: 'https://avatars.githubusercontent.com/u/119868298?v=4',
  description: 'Personal site and blog',
  keywords: 'workouts, running, cycling, riding, roadtrip, hiking, swimming',
  navLinks: [
    {
      name: 'Blog',
      url: 'https://flyfish321.github.io/gitblog/',
    },
    {
      name: 'About',
      url: 'https://github.com/flyfish321/workouts_map/blob/master/README-CN.md',
    },
  ],
};

export default data;
