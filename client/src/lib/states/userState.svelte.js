let user = $state({ });

const useUserState = () => {
  return {
    get user() {
      return user;
    },
    set user(u) {
      user = u;
    },
  }; // you can also define other methods/properties here
};

export { useUserState };