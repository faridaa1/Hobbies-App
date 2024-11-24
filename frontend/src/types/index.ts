export interface CustomUser {
    id: number;
    name: string;
    email: string;
    date_of_birth: string;
    hobbies: UserHobby[];
    friends: Friendship[];
    profile_picture: string | null
}

export interface Hobby {
    id: number;
    name: string;
    description: string
}

export interface UserHobby { 
    user: number;
    hobby: number;
    level: 'Beginner' | 'Intermediate' | 'Advanced';
    start_date: string
}

export interface Friendship {
    user1: number;
    user2: number;
    status: 'Pending' | 'Accepted'
}