from typing import List, Optional

from sqlalchemy import Boolean, Column, DateTime, Double, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


class Cores(Base):
    __tablename__ = 'cores'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='cores_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    serial: Mapped[Optional[str]] = mapped_column(String)
    status: Mapped[Optional[str]] = mapped_column(String)
    reuse_count: Mapped[Optional[int]] = mapped_column(Integer)
    asds_attempts: Mapped[Optional[int]] = mapped_column(Integer)
    asds_landings: Mapped[Optional[int]] = mapped_column(Integer)
    rtls_attempts: Mapped[Optional[int]] = mapped_column(Integer)
    rtls_landings: Mapped[Optional[int]] = mapped_column(Integer)

    launch_cores: Mapped[List['LaunchCores']] = relationship('LaunchCores', back_populates='core')


class Launchpads(Base):
    __tablename__ = 'launchpads'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='launchpads_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String)
    locality: Mapped[Optional[str]] = mapped_column(String)
    region: Mapped[Optional[str]] = mapped_column(String)
    status: Mapped[Optional[str]] = mapped_column(String)

    launches: Mapped[List['Launches']] = relationship('Launches', back_populates='launchpad')


class Rockets(Base):
    __tablename__ = 'rockets'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='rockets_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String)
    height: Mapped[Optional[float]] = mapped_column(Double(53))
    mass: Mapped[Optional[float]] = mapped_column(Double(53))
    cost_per_launch: Mapped[Optional[float]] = mapped_column(Double(53))

    launches: Mapped[List['Launches']] = relationship('Launches', back_populates='rocket')


class Launches(Base):
    __tablename__ = 'launches'
    __table_args__ = (
        ForeignKeyConstraint(['launchpad_id'], ['public.launchpads.id'], name='launches_launchpad_id_fkey'),
        ForeignKeyConstraint(['rocket_id'], ['public.rockets.id'], name='launches_rocket_id_fkey'),
        PrimaryKeyConstraint('id', name='launches_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    date_utc: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    success: Mapped[Optional[bool]] = mapped_column(Boolean)
    rocket_id: Mapped[Optional[str]] = mapped_column(String)
    launchpad_id: Mapped[Optional[str]] = mapped_column(String)

    launchpad: Mapped[Optional['Launchpads']] = relationship('Launchpads', back_populates='launches')
    rocket: Mapped[Optional['Rockets']] = relationship('Rockets', back_populates='launches')
    payload: Mapped[List['Payloads']] = relationship('Payloads', secondary='public.launch_payloads', back_populates='launch')
    crew: Mapped[List['Crew']] = relationship('Crew', back_populates='launch')
    launch_cores: Mapped[List['LaunchCores']] = relationship('LaunchCores', back_populates='launch')
    payloads: Mapped[List['Payloads']] = relationship('Payloads', back_populates='launch_')
    starlink_satellites: Mapped[List['StarlinkSatellites']] = relationship('StarlinkSatellites', back_populates='launch')


class Crew(Base):
    __tablename__ = 'crew'
    __table_args__ = (
        ForeignKeyConstraint(['launch_id'], ['public.launches.id'], name='crew_launch_id_fkey'),
        PrimaryKeyConstraint('id', name='crew_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String)
    status: Mapped[Optional[str]] = mapped_column(String)
    launch_id: Mapped[Optional[str]] = mapped_column(String)

    launch: Mapped[Optional['Launches']] = relationship('Launches', back_populates='crew')


class LaunchCores(Base):
    __tablename__ = 'launch_cores'
    __table_args__ = (
        ForeignKeyConstraint(['core_id'], ['public.cores.id'], name='launch_cores_core_id_fkey'),
        ForeignKeyConstraint(['launch_id'], ['public.launches.id'], name='launch_cores_launch_id_fkey'),
        PrimaryKeyConstraint('launch_id', 'core_id', name='launch_cores_pkey'),
        {'schema': 'public'}
    )

    launch_id: Mapped[str] = mapped_column(String, primary_key=True)
    core_id: Mapped[str] = mapped_column(String, primary_key=True)
    flight_number: Mapped[Optional[int]] = mapped_column(Integer)
    reused: Mapped[Optional[bool]] = mapped_column(Boolean)
    land_success: Mapped[Optional[bool]] = mapped_column(Boolean)

    core: Mapped['Cores'] = relationship('Cores', back_populates='launch_cores')
    launch: Mapped['Launches'] = relationship('Launches', back_populates='launch_cores')


class Payloads(Base):
    __tablename__ = 'payloads'
    __table_args__ = (
        ForeignKeyConstraint(['launch_id'], ['public.launches.id'], name='payloads_launch_id_fkey'),
        PrimaryKeyConstraint('id', name='payloads_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    launch_id: Mapped[str] = mapped_column(String)
    type: Mapped[Optional[str]] = mapped_column(String)
    mass_kg: Mapped[Optional[float]] = mapped_column(Double(53))
    orbit: Mapped[Optional[str]] = mapped_column(String)

    launch: Mapped[List['Launches']] = relationship('Launches', secondary='public.launch_payloads', back_populates='payload')
    launch_: Mapped['Launches'] = relationship('Launches', back_populates='payloads')


class StarlinkSatellites(Base):
    __tablename__ = 'starlink_satellites'
    __table_args__ = (
        ForeignKeyConstraint(['launch_id'], ['public.launches.id'], name='starlink_satellites_launch_id_fkey'),
        PrimaryKeyConstraint('id', name='starlink_satellites_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    height_km: Mapped[Optional[float]] = mapped_column(Double(53))
    latitude: Mapped[Optional[float]] = mapped_column(Double(53))
    longitude: Mapped[Optional[float]] = mapped_column(Double(53))
    velocity_kms: Mapped[Optional[float]] = mapped_column(Double(53))
    version: Mapped[Optional[str]] = mapped_column(String)
    launch_id: Mapped[Optional[str]] = mapped_column(String)
    decayed: Mapped[Optional[bool]] = mapped_column(Boolean)

    launch: Mapped[Optional['Launches']] = relationship('Launches', back_populates='starlink_satellites')
    orbital_parameters: Mapped[List['OrbitalParameters']] = relationship('OrbitalParameters', back_populates='starlink')


t_launch_payloads = Table(
    'launch_payloads', Base.metadata,
    Column('launch_id', String, primary_key=True, nullable=False),
    Column('payload_id', String, primary_key=True, nullable=False),
    ForeignKeyConstraint(['launch_id'], ['public.launches.id'], name='launch_payloads_launch_id_fkey'),
    ForeignKeyConstraint(['payload_id'], ['public.payloads.id'], name='launch_payloads_payload_id_fkey'),
    PrimaryKeyConstraint('launch_id', 'payload_id', name='launch_payloads_pkey'),
    schema='public'
)


class OrbitalParameters(Base):
    __tablename__ = 'orbital_parameters'
    __table_args__ = (
        ForeignKeyConstraint(['starlink_id'], ['public.starlink_satellites.id'], name='orbital_parameters_starlink_id_fkey'),
        PrimaryKeyConstraint('norad_cat_id', name='orbital_parameters_pkey'),
        {'schema': 'public'}
    )

    norad_cat_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    starlink_id: Mapped[str] = mapped_column(String)
    object_name: Mapped[Optional[str]] = mapped_column(String)
    inclination: Mapped[Optional[float]] = mapped_column(Double(53))
    semimajor_axis: Mapped[Optional[float]] = mapped_column(Double(53))
    period: Mapped[Optional[float]] = mapped_column(Double(53))
    eccentricity: Mapped[Optional[float]] = mapped_column(Double(53))
    epoch: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    mean_motion: Mapped[Optional[float]] = mapped_column(Double(53))
    country_code: Mapped[Optional[str]] = mapped_column(String(3))

    starlink: Mapped['StarlinkSatellites'] = relationship('StarlinkSatellites', back_populates='orbital_parameters')
