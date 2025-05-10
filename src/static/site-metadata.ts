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

const getBasePath = () => {
  const baseUrl = import.meta.env.BASE_URL;
  return baseUrl === '/' ? '' : baseUrl;
};

const data: ISiteMetadataResult = {
  siteTitle: 'Workouts Map',
  siteUrl: 'https://flyfish321.github.io/workouts_map/',
  logo: 'https://avatars.githubusercontent.com/u/119868298?s=400&u=c24ba15fe9ce0ebbe8ae7f1d59da2b91215a9edf&v=4',
  description: 'Personal site and blog',
  keywords: 'workouts, running, cycling, riding, roadtrip, hiking, swimming',
  navLinks: [
    {
      name: 'Summary',
      url: `${getBasePath()}/summary`,
    },
    {
      name: 'Blog',
      url: 'https://www.yhyblog.com',
    },
    {
      name: 'About',
      url: 'https://www.yhyblog.com/index.php/about.html',
    },
  ],
};

export default data;
