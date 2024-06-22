export const $Body_login_access_token = {
	properties: {
		grant_type: {
	type: 'any-of',
	contains: [{
	type: 'string',
	pattern: 'password',
}, {
	type: 'null',
}],
},
		username: {
	type: 'string',
	isRequired: true,
},
		password: {
	type: 'string',
	isRequired: true,
},
		scope: {
	type: 'string',
	default: '',
},
		client_id: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'null',
}],
},
		client_secret: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'null',
}],
},
	},
} as const;

export const $HTTPValidationError = {
	properties: {
		detail: {
	type: 'array',
	contains: {
		type: 'ValidationError',
	},
},
	},
} as const;

export const $IDeleteResponseBase_IOzonDataRead_ = {
	properties: {
		message: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'null',
}],
},
		meta: {
	type: 'any-of',
	contains: [{
	type: 'dictionary',
	contains: {
	properties: {
	},
},
}, {
	properties: {
	},
}, {
	type: 'null',
}],
},
		data: {
	type: 'any-of',
	contains: [{
	type: 'IOzonDataRead',
}, {
	type: 'null',
}],
},
	},
} as const;

export const $IDeleteResponseBase_IOzonReportRead_ = {
	properties: {
		message: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'null',
}],
},
		meta: {
	type: 'any-of',
	contains: [{
	type: 'dictionary',
	contains: {
	properties: {
	},
},
}, {
	properties: {
	},
}, {
	type: 'null',
}],
},
		data: {
	type: 'any-of',
	contains: [{
	type: 'IOzonReportRead',
}, {
	type: 'null',
}],
},
	},
} as const;

export const $IDeleteResponseBase_IUserRead_ = {
	properties: {
		message: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'null',
}],
},
		meta: {
	type: 'any-of',
	contains: [{
	type: 'dictionary',
	contains: {
	properties: {
	},
},
}, {
	properties: {
	},
}, {
	type: 'null',
}],
},
		data: {
	type: 'any-of',
	contains: [{
	type: 'IUserRead',
}, {
	type: 'null',
}],
},
	},
} as const;

export const $IGetResponseBase_IOzonDataRead_ = {
	properties: {
		message: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'null',
}],
},
		meta: {
	type: 'any-of',
	contains: [{
	type: 'dictionary',
	contains: {
	properties: {
	},
},
}, {
	properties: {
	},
}, {
	type: 'null',
}],
},
		data: {
	type: 'any-of',
	contains: [{
	type: 'IOzonDataRead',
}, {
	type: 'null',
}],
},
	},
} as const;

export const $IGetResponseBase_IRoleRead_ = {
	properties: {
		message: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'null',
}],
},
		meta: {
	type: 'any-of',
	contains: [{
	type: 'dictionary',
	contains: {
	properties: {
	},
},
}, {
	properties: {
	},
}, {
	type: 'null',
}],
},
		data: {
	type: 'any-of',
	contains: [{
	type: 'IRoleRead',
}, {
	type: 'null',
}],
},
	},
} as const;

export const $IGetResponseBase_IUserReadWithRole_ = {
	properties: {
		message: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'null',
}],
},
		meta: {
	type: 'any-of',
	contains: [{
	type: 'dictionary',
	contains: {
	properties: {
	},
},
}, {
	properties: {
	},
}, {
	type: 'null',
}],
},
		data: {
	type: 'any-of',
	contains: [{
	type: 'IUserReadWithRole',
}, {
	type: 'null',
}],
},
	},
} as const;

export const $IGetResponsePaginated_IOzonReportRead_ = {
	properties: {
		items: {
	type: 'array',
	contains: {
		type: 'IOzonReportRead',
	},
	isRequired: true,
},
		total: {
	type: 'any-of',
	contains: [{
	type: 'number',
	minimum: 0,
}, {
	type: 'null',
}],
	isRequired: true,
},
		page: {
	type: 'any-of',
	contains: [{
	type: 'number',
	minimum: 1,
}, {
	type: 'null',
}],
	isRequired: true,
},
		size: {
	type: 'any-of',
	contains: [{
	type: 'number',
	minimum: 1,
}, {
	type: 'null',
}],
	isRequired: true,
},
		pages: {
	type: 'any-of',
	contains: [{
	type: 'number',
	minimum: 0,
}, {
	type: 'null',
}],
},
		links: {
	type: 'Links',
	isRequired: true,
},
		message: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'null',
}],
},
		meta: {
	type: 'any-of',
	contains: [{
	type: 'dictionary',
	contains: {
	properties: {
	},
},
}, {
	properties: {
	},
}, {
	type: 'null',
}],
},
	},
} as const;

export const $IGetResponsePaginated_IRoleRead_ = {
	properties: {
		items: {
	type: 'array',
	contains: {
		type: 'IRoleRead',
	},
	isRequired: true,
},
		total: {
	type: 'any-of',
	contains: [{
	type: 'number',
	minimum: 0,
}, {
	type: 'null',
}],
	isRequired: true,
},
		page: {
	type: 'any-of',
	contains: [{
	type: 'number',
	minimum: 1,
}, {
	type: 'null',
}],
	isRequired: true,
},
		size: {
	type: 'any-of',
	contains: [{
	type: 'number',
	minimum: 1,
}, {
	type: 'null',
}],
	isRequired: true,
},
		pages: {
	type: 'any-of',
	contains: [{
	type: 'number',
	minimum: 0,
}, {
	type: 'null',
}],
},
		links: {
	type: 'Links',
	isRequired: true,
},
		message: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'null',
}],
},
		meta: {
	type: 'any-of',
	contains: [{
	type: 'dictionary',
	contains: {
	properties: {
	},
},
}, {
	properties: {
	},
}, {
	type: 'null',
}],
},
	},
} as const;

export const $IGetResponsePaginated_IUserReadWithRole_ = {
	properties: {
		items: {
	type: 'array',
	contains: {
		type: 'IUserReadWithRole',
	},
	isRequired: true,
},
		total: {
	type: 'any-of',
	contains: [{
	type: 'number',
	minimum: 0,
}, {
	type: 'null',
}],
	isRequired: true,
},
		page: {
	type: 'any-of',
	contains: [{
	type: 'number',
	minimum: 1,
}, {
	type: 'null',
}],
	isRequired: true,
},
		size: {
	type: 'any-of',
	contains: [{
	type: 'number',
	minimum: 1,
}, {
	type: 'null',
}],
	isRequired: true,
},
		pages: {
	type: 'any-of',
	contains: [{
	type: 'number',
	minimum: 0,
}, {
	type: 'null',
}],
},
		links: {
	type: 'Links',
	isRequired: true,
},
		message: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'null',
}],
},
		meta: {
	type: 'any-of',
	contains: [{
	type: 'dictionary',
	contains: {
	properties: {
	},
},
}, {
	properties: {
	},
}, {
	type: 'null',
}],
},
	},
} as const;

export const $IOzonDataCreate = {
	properties: {
		client_id: {
	type: 'string',
	isRequired: true,
},
		api_key: {
	type: 'string',
	isRequired: true,
},
	},
} as const;

export const $IOzonDataRead = {
	properties: {
		client_id: {
	type: 'string',
	isRequired: true,
},
		api_key: {
	type: 'string',
	isRequired: true,
},
		user_id: {
	type: 'any-of',
	contains: [{
	type: 'string',
	format: 'uuid',
}, {
	type: 'null',
}],
},
		id: {
	type: 'string',
	isRequired: true,
	format: 'uuid',
},
	},
} as const;

export const $IOzonReportRead = {
	properties: {
		report_type: {
	type: 'string',
	isRequired: true,
},
		ozon_created_at: {
	type: 'any-of',
	contains: [{
	type: 'string',
	format: 'date-time',
}, {
	type: 'null',
}],
	isRequired: true,
},
		id: {
	type: 'string',
	isRequired: true,
	format: 'uuid',
},
		created_at: {
	type: 'any-of',
	contains: [{
	type: 'string',
	format: 'date-time',
}, {
	type: 'null',
}],
	isRequired: true,
},
	},
} as const;

export const $IPostResponseBase_IOzonDataRead_ = {
	properties: {
		message: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'null',
}],
},
		meta: {
	type: 'any-of',
	contains: [{
	type: 'dictionary',
	contains: {
	properties: {
	},
},
}, {
	properties: {
	},
}, {
	type: 'null',
}],
},
		data: {
	type: 'any-of',
	contains: [{
	type: 'IOzonDataRead',
}, {
	type: 'null',
}],
},
	},
} as const;

export const $IPostResponseBase_IRoleRead_ = {
	properties: {
		message: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'null',
}],
},
		meta: {
	type: 'any-of',
	contains: [{
	type: 'dictionary',
	contains: {
	properties: {
	},
},
}, {
	properties: {
	},
}, {
	type: 'null',
}],
},
		data: {
	type: 'any-of',
	contains: [{
	type: 'IRoleRead',
}, {
	type: 'null',
}],
},
	},
} as const;

export const $IPostResponseBase_IUserRead_ = {
	properties: {
		message: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'null',
}],
},
		meta: {
	type: 'any-of',
	contains: [{
	type: 'dictionary',
	contains: {
	properties: {
	},
},
}, {
	properties: {
	},
}, {
	type: 'null',
}],
},
		data: {
	type: 'any-of',
	contains: [{
	type: 'IUserRead',
}, {
	type: 'null',
}],
},
	},
} as const;

export const $IPutResponseBase_IRoleRead_ = {
	properties: {
		message: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'null',
}],
},
		meta: {
	type: 'any-of',
	contains: [{
	type: 'dictionary',
	contains: {
	properties: {
	},
},
}, {
	properties: {
	},
}, {
	type: 'null',
}],
},
		data: {
	type: 'any-of',
	contains: [{
	type: 'IRoleRead',
}, {
	type: 'null',
}],
},
	},
} as const;

export const $IPutResponseBase_IUserRead_ = {
	properties: {
		message: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'null',
}],
},
		meta: {
	type: 'any-of',
	contains: [{
	type: 'dictionary',
	contains: {
	properties: {
	},
},
}, {
	properties: {
	},
}, {
	type: 'null',
}],
},
		data: {
	type: 'any-of',
	contains: [{
	type: 'IUserRead',
}, {
	type: 'null',
}],
},
	},
} as const;

export const $IRoleCreate = {
	properties: {
		name: {
	type: 'string',
	isRequired: true,
},
		description: {
	type: 'string',
	isRequired: true,
},
	},
} as const;

export const $IRoleRead = {
	properties: {
		name: {
	type: 'string',
	isRequired: true,
},
		description: {
	type: 'string',
	isRequired: true,
},
		id: {
	type: 'string',
	isRequired: true,
	format: 'uuid',
},
	},
} as const;

export const $IUserCreate = {
	properties: {
		name: {
	type: 'string',
	isRequired: true,
},
		surname: {
	type: 'string',
	isRequired: true,
},
		email: {
	type: 'string',
	isRequired: true,
	format: 'email',
},
		is_active: {
	type: 'boolean',
	default: true,
},
		role_id: {
	type: 'any-of',
	contains: [{
	type: 'string',
	format: 'uuid',
}, {
	type: 'null',
}],
},
		password: {
	type: 'string',
	isRequired: true,
},
	},
} as const;

export const $IUserRead = {
	properties: {
		name: {
	type: 'string',
	isRequired: true,
},
		surname: {
	type: 'string',
	isRequired: true,
},
		email: {
	type: 'string',
	isRequired: true,
	format: 'email',
},
		is_active: {
	type: 'boolean',
	default: true,
},
		role_id: {
	type: 'any-of',
	contains: [{
	type: 'string',
	format: 'uuid',
}, {
	type: 'null',
}],
},
		id: {
	type: 'string',
	isRequired: true,
	format: 'uuid',
},
	},
} as const;

export const $IUserReadWithRole = {
	properties: {
		name: {
	type: 'string',
	isRequired: true,
},
		surname: {
	type: 'string',
	isRequired: true,
},
		email: {
	type: 'string',
	isRequired: true,
	format: 'email',
},
		is_active: {
	type: 'boolean',
	default: true,
},
		role_id: {
	type: 'any-of',
	contains: [{
	type: 'string',
	format: 'uuid',
}, {
	type: 'null',
}],
},
		id: {
	type: 'string',
	isRequired: true,
	format: 'uuid',
},
		role: {
	type: 'IRoleRead',
	isRequired: true,
},
	},
} as const;

export const $IUserStatus = {
	type: 'Enum',
	enum: ['active','inactive',],
} as const;

export const $IUserUpdateMe = {
	properties: {
		name: {
	type: 'any-of',
	contains: [{
	type: 'string',
	minLength: 1,
}, {
	type: 'null',
}],
},
		surname: {
	type: 'any-of',
	contains: [{
	type: 'string',
	minLength: 1,
}, {
	type: 'null',
}],
},
	},
} as const;

export const $IUserUpdatePassword = {
	properties: {
		current_password: {
	type: 'string',
	isRequired: true,
},
		new_password: {
	type: 'string',
	isRequired: true,
},
	},
} as const;

export const $Links = {
	properties: {
		first: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'null',
}],
	isRequired: true,
},
		last: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'null',
}],
	isRequired: true,
},
		self: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'null',
}],
	isRequired: true,
},
		next: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'null',
}],
	isRequired: true,
},
		prev: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'null',
}],
	isRequired: true,
},
	},
} as const;

export const $MessageResponse = {
	properties: {
		message: {
	type: 'string',
	isRequired: true,
},
	},
} as const;

export const $PartialIOzonDataUpdate = {
	properties: {
		client_id: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'null',
}],
},
		api_key: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'null',
}],
},
	},
} as const;

export const $PartialIRoleUpdate = {
	properties: {
		description: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'null',
}],
},
	},
} as const;

export const $PartialIUserUpdate = {
	properties: {
		name: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'null',
}],
},
		surname: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'null',
}],
},
		email: {
	type: 'any-of',
	contains: [{
	type: 'string',
	format: 'email',
}, {
	type: 'null',
}],
},
		is_active: {
	type: 'any-of',
	contains: [{
	type: 'boolean',
}, {
	type: 'null',
}],
},
		role_id: {
	type: 'any-of',
	contains: [{
	type: 'string',
	format: 'uuid',
}, {
	type: 'null',
}],
},
		password: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'null',
}],
},
		role: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'null',
}],
},
	},
} as const;

export const $Token = {
	properties: {
		access_token: {
	type: 'string',
	isRequired: true,
},
		token_type: {
	type: 'string',
	default: 'bearer',
},
	},
} as const;

export const $ValidationError = {
	properties: {
		loc: {
	type: 'array',
	contains: {
	type: 'any-of',
	contains: [{
	type: 'string',
}, {
	type: 'number',
}],
},
	isRequired: true,
},
		msg: {
	type: 'string',
	isRequired: true,
},
		type: {
	type: 'string',
	isRequired: true,
},
	},
} as const;