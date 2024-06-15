export type Body_login_access_token = {
	grant_type?: string | null;
	username: string;
	password: string;
	scope?: string;
	client_id?: string | null;
	client_secret?: string | null;
};



export type HTTPValidationError = {
	detail?: Array<ValidationError>;
};



export type IDeleteResponseBase_IOzonDataRead_ = {
	message?: string | null;
	meta?: Record<string, unknown> | unknown | null;
	data?: IOzonDataRead | null;
};



export type IDeleteResponseBase_IOzonReportRead_ = {
	message?: string | null;
	meta?: Record<string, unknown> | unknown | null;
	data?: IOzonReportRead | null;
};



export type IDeleteResponseBase_IUserRead_ = {
	message?: string | null;
	meta?: Record<string, unknown> | unknown | null;
	data?: IUserRead | null;
};



export type IGetResponseBase_IOzonDataRead_ = {
	message?: string | null;
	meta?: Record<string, unknown> | unknown | null;
	data?: IOzonDataRead | null;
};



export type IGetResponseBase_IRoleRead_ = {
	message?: string | null;
	meta?: Record<string, unknown> | unknown | null;
	data?: IRoleRead | null;
};



export type IGetResponseBase_IUserReadWithRole_ = {
	message?: string | null;
	meta?: Record<string, unknown> | unknown | null;
	data?: IUserReadWithRole | null;
};



export type IGetResponsePaginated_IOzonReportRead_ = {
	items: Array<IOzonReportRead>;
	total: number | null;
	page: number | null;
	size: number | null;
	pages?: number | null;
	links: Links;
	message?: string | null;
	meta?: Record<string, unknown> | unknown | null;
};



export type IGetResponsePaginated_IRoleRead_ = {
	items: Array<IRoleRead>;
	total: number | null;
	page: number | null;
	size: number | null;
	pages?: number | null;
	links: Links;
	message?: string | null;
	meta?: Record<string, unknown> | unknown | null;
};



export type IGetResponsePaginated_IUserReadWithRole_ = {
	items: Array<IUserReadWithRole>;
	total: number | null;
	page: number | null;
	size: number | null;
	pages?: number | null;
	links: Links;
	message?: string | null;
	meta?: Record<string, unknown> | unknown | null;
};



export type IOzonDataCreate = {
	client_id: string;
	api_key: string;
};



export type IOzonDataRead = {
	client_id: string;
	api_key: string;
	user_id?: string | null;
	id: string;
};



export type IOzonReportRead = {
	report_type: string;
	ozon_created_at: string | null;
	id: string;
};



export type IPostResponseBase_IOzonDataRead_ = {
	message?: string | null;
	meta?: Record<string, unknown> | unknown | null;
	data?: IOzonDataRead | null;
};



export type IPostResponseBase_IRoleRead_ = {
	message?: string | null;
	meta?: Record<string, unknown> | unknown | null;
	data?: IRoleRead | null;
};



export type IPostResponseBase_IUserRead_ = {
	message?: string | null;
	meta?: Record<string, unknown> | unknown | null;
	data?: IUserRead | null;
};



export type IPutResponseBase_IRoleRead_ = {
	message?: string | null;
	meta?: Record<string, unknown> | unknown | null;
	data?: IRoleRead | null;
};



export type IPutResponseBase_IUserRead_ = {
	message?: string | null;
	meta?: Record<string, unknown> | unknown | null;
	data?: IUserRead | null;
};



export type IRoleCreate = {
	name: string;
	description: string;
};



export type IRoleRead = {
	name: string;
	description: string;
	id: string;
};



export type IUserCreate = {
	name: string;
	surname: string;
	email: string;
	is_active?: boolean;
	role_id?: string | null;
	password: string;
};



export type IUserRead = {
	name: string;
	surname: string;
	email: string;
	is_active?: boolean;
	role_id?: string | null;
	id: string;
};



export type IUserReadWithRole = {
	name: string;
	surname: string;
	email: string;
	is_active?: boolean;
	role_id?: string | null;
	id: string;
	role: IRoleRead;
};



export type IUserStatus = 'active' | 'inactive';



export type IUserUpdateMe = {
	name?: string | null;
	surname?: string | null;
};



export type IUserUpdatePassword = {
	current_password: string;
	new_password: string;
};



export type Links = {
	first: string | null;
	last: string | null;
	self: string | null;
	next: string | null;
	prev: string | null;
};



export type MessageResponse = {
	message: string;
};



export type PartialIOzonDataUpdate = {
	client_id?: string | null;
	api_key?: string | null;
};



export type PartialIRoleUpdate = {
	description?: string | null;
};



export type PartialIUserUpdate = {
	name?: string | null;
	surname?: string | null;
	email?: string | null;
	is_active?: boolean | null;
	role_id?: string | null;
	password?: string | null;
};



export type Token = {
	access_token: string;
	token_type?: string;
};



export type ValidationError = {
	loc: Array<string | number>;
	msg: string;
	type: string;
};

